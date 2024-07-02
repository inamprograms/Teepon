from dotenv import load_dotenv
from helper import *

import mysql.connector
import random
import os

logger = logging.getLogger()
load_dotenv()

def main():
    config = yaml.load(open("config.yaml", "r"), Loader=yaml.FullLoader)
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    logging.basicConfig(
        format="%(message)s",
        handlers=[logging.StreamHandler(ColorPrint())],
    )
    logger.setLevel(logging.INFO)

    scenario = input(
        "Please select a scenario (calendar/maps): "
    )

    scenario = scenario.lower()
    api_spec, headers = None, None

    # database connection details
    db_config = {
        'host': os.getenv("MYSQL_HOST"),
        'database': os.getenv("MYSQL_DATABASE"),
        'user': os.getenv("MYSQL_USER"),
        'password': os.getenv("MYSQL_PASSWORD"),
    }

    # Connect to the MySQL server
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    user_id = int(input("Enter the user id: "))

    if scenario == "calendar":
        if user_id is not None:
            try:
                ser_qu = f"SELECT * FROM credentials WHERE user_id = {user_id};"
                cursor.execute(ser_qu)
                res = cursor.fetchone()
                res_t = res[2]
                print(f"your token {res_t}")
                os.environ["GOOGLE_TOKEN"] = res_t
                dic = {
                    "user_id": user_id,
                    "your_token": res_t
                }
                print(dic)
            except:
                print("Key is not present in the database")
                return ""

        else:
            print("Your id is incorrect.")

        api_spec, headers = process_spec_file(
            file_path="specs/calendar_oas.json", token=os.environ["GOOGLE_TOKEN"]
        )
        query_example = "What events do I have today?"

    elif scenario == "teepon":
        api_spec, headers = process_spec_file(
            file_path="specs/teapon_oas.json"
        )
        headers = {}
    else:
        raise ValueError(f"Unsupported scenario: {scenario}")

    populate_api_selector_icl_examples(scenario=scenario)
    populate_planner_icl_examples(scenario=scenario)

    requests_wrapper = Requests(headers=headers)

    # text-davinci-003

    llm = OpenAI(model_name="gpt-4", temperature=0.0, max_tokens=1024)
    api_llm = ApiLLM(
        llm,
        api_spec=api_spec,
        scenario=scenario,
        requests_wrapper=requests_wrapper,
        simple_parser=False,
    )

    print(f"Example instruction: {query_example}")
    query = input(
        "Please input an instruction (Press ENTER to use the example instruction): "
    )
    if query == "":
        query = query_example

    logger.info(f"Query: {query}")

    start_time = time.time()
    api_llm.run(query)
    logger.info(f"Execution Time: {time.time() - start_time}")


if __name__ == "__main__":
    main()

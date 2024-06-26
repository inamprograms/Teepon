// src/store/chatSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [],
  currentRoom: "",
  socketId: "",
  user: null,
  server_url: "http://localhost:10000/api",
  userdata:null
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addMessage: (state, action) => {
      const { message, sender } = action.payload;
      state.messages.push({ message, sender });
    },
    setCurrentRoom: (state, action) => {
      state.currentRoom = action.payload;
    },
    setCurrentMessages: (state, action) => {
      state.messages = action.payload;
    },
    setSocketId: (state, action) => {
      state.socketId = action.payload;
    },
    setUser: (state, action) => {
      state.user = action.payload;
     // console.log("from redux,", action.payload);
    },
    clearUser: (state) => {
      state.user = null;
    },
    setUserdata: (state, action) => {
      state.userdata = action.payload;
      console.log("from redux,", action.payload);
    },
  },
});

export const { addMessage,setUserdata, setCurrentRoom, setSocketId, setUser, clearUser, setCurrentMessages, server_url } =
  chatSlice.actions;

export default chatSlice.reducer;

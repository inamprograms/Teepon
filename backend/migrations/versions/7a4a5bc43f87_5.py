"""5

Revision ID: 7a4a5bc43f87
Revises: 14b9cca7cafb
Create Date: 2024-06-30 00:53:28.148101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a4a5bc43f87'
down_revision = '14b9cca7cafb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ai_messages',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('ai_message_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ai_message_id'], ['ai_message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('ai_messages')
    # ### end Alembic commands ###

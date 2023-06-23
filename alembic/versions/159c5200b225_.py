"""empty message

Revision ID: 159c5200b225
Revises: b5efa5dde09d
Create Date: 2023-06-22 11:07:17.519162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '159c5200b225'
down_revision = 'b5efa5dde09d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'daily_checklist', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'daily_checklist', type_='unique')
    # ### end Alembic commands ###
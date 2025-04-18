"""add restaurant_id column in Orders

Revision ID: d63213c74435
Revises: e3ffae01956a
Create Date: 2024-12-06 21:05:30.338265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd63213c74435'
down_revision: Union[str, None] = 'e3ffae01956a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('restaurant_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'orders', 'restaurants', ['restaurant_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'restaurant_id')
    # ### end Alembic commands ###

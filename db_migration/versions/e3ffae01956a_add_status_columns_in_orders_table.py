"""add status columns in Orders table

Revision ID: e3ffae01956a
Revises: 1f2d44c8fb8e
Create Date: 2024-12-06 19:42:03.917790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = 'e3ffae01956a'
down_revision: Union[str, None] = '1f2d44c8fb8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_enum = ENUM(
    'in_progress', 'done',
    name='orderstatus',
    create_type=False
)

order_acceptance_enum = ENUM(
    'pending', 'accepted', 'rejected',
    name='acceptancestatus',
    create_type=False
)

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Create the ENUM type if it doesn't exist
    order_status_enum.create(op.get_bind(), checkfirst=True)
    order_acceptance_enum.create(op.get_bind(), checkfirst=True)
    
    op.add_column('orders', sa.Column('order_status', sa.Enum('in_progress', 'done', name='orderstatus'), server_default='in_progress', nullable=False))
    op.add_column('orders', sa.Column('acceptance_status', sa.Enum('pending', 'accepted', 'rejected', name='acceptancestatus'), server_default='pending', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'acceptance_status')
    op.drop_column('orders', 'order_status')
    
    # Drop the ENUM type if it exists
    order_status_enum.drop(op.get_bind(), checkfirst=True)
    order_acceptance_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###

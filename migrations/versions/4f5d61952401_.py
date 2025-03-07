"""empty message

Revision ID: 4f5d61952401
Revises: 7367fa5c2b29
Create Date: 2024-12-21 16:20:32.049739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4f5d61952401'
down_revision: Union[str, None] = '7367fa5c2b29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'photo',
               existing_type=postgresql.BYTEA(),
               type_=sa.String(),
               existing_nullable=True)
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.alter_column('user', 'photo',
               existing_type=sa.String(),
               type_=postgresql.BYTEA(),
               existing_nullable=True)
    # ### end Alembic commands ###

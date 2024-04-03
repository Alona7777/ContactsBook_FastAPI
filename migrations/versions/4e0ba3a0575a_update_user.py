"""update user

Revision ID: 4e0ba3a0575a
Revises: 2eb386bf26ce
Create Date: 2024-04-02 13:53:40.243424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4e0ba3a0575a'
down_revision: Union[str, None] = '2eb386bf26ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('avatar', sa.String(length=255), nullable=True))
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('admin', 'moderator', 'user', name='role'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('admin', 'moderator', 'user', name='role'),
               nullable=True)
    op.drop_column('users', 'avatar')
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###

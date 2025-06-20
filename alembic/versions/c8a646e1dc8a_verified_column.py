"""verified column

Revision ID: c8a646e1dc8a
Revises: 256f22848ca1
Create Date: 2025-06-16 23:21:41.373925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8a646e1dc8a'
down_revision: Union[str, None] = '256f22848ca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('verified', sa.Boolean(), server_default='false', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'verified')
    # ### end Alembic commands ###

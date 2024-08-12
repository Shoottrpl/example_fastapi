"""add lasst few column to posts table

Revision ID: c73c10c97076
Revises: f6d6c6be2515
Create Date: 2024-08-12 23:05:48.094255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c73c10c97076'
down_revision: Union[str, None] = 'f6d6c6be2515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published",
                                     sa.Boolean(), nullable=False,
                                     server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                                     nullable=False,
                                     server_default=sa.text("now()")), )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass

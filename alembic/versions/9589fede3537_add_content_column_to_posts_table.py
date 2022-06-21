"""add content column to posts table

Revision ID: 9589fede3537
Revises: 4f864c974cba
Create Date: 2022-06-20 14:35:18.483548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9589fede3537'
down_revision = '4f864c974cba'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass

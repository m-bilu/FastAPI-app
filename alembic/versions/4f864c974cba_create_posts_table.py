"""create posts table

Revision ID: 4f864c974cba
Revises: 
Create Date: 2022-06-20 13:15:32.012173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f864c974cba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key = True)
    , sa.Column("title", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass

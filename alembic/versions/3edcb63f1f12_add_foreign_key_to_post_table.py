"""add foreign key to post table

Revision ID: 3edcb63f1f12
Revises: 8cb6e8da5c81
Create Date: 2022-06-20 14:53:38.389367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3edcb63f1f12'
down_revision = '8cb6e8da5c81'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("userid", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", 
    local_cols=["userid"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "userid")
    pass

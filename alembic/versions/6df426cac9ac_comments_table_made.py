"""Comments Table made

Revision ID: 6df426cac9ac
Revises: cf0e02a23988
Create Date: 2022-06-22 11:50:24.178001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6df426cac9ac'
down_revision = 'cf0e02a23988'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("comments", 
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("postid", sa.Integer(), nullable=False),
    sa.Column("userid", sa.Integer(), nullable=False),
    sa.Column("content", sa.String(), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
        server_default=sa.text("now()"), nullable=False),
    sa.PrimaryKeyConstraint("id"), # ID IS PRIMARY KEY
    )
    pass


def downgrade():
    op.drop_table("comments")
    pass

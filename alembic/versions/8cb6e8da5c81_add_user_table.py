"""add user table

Revision ID: 8cb6e8da5c81
Revises: 9589fede3537
Create Date: 2022-06-20 14:39:35.899694

"""
from alembic import op
import sqlalchemy as sa # OBJECT to use sqlalchemy functions with


# revision identifiers, used by Alembic.
revision = '8cb6e8da5c81'
down_revision = '9589fede3537'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", 
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("email", sa.String(), nullable=False),
    sa.Column("password", sa.String(), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), 
        server_default=sa.text("now()"), nullable=False),
    sa.PrimaryKeyConstraint("id"), # ID IS PRIMARY KEY
    sa.UniqueConstraint("email") # EMAIL NEEDS TO BE UNIQUE
    )
    pass


def downgrade():
    op.drop_table("users")
    pass

"""create_user_table

Revision ID: e2062fdff483
Revises:
Create Date: 2017-03-30 19:37:56.667449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2062fdff483'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(255), nullable=False),
        sa.Column('last_name', sa.String(255), nullable=True),
        sa.Column('username', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('birth_date', sa.Date, nullable=True),
        sa.Column('landline_number', sa.String(255), nullable=True),
        sa.Column('mobile_number', sa.String(255), nullable=True),
        sa.Column('image_url', sa.String(255), nullable=True),
        sa.Column('status', sa.String(255), nullable=True),
        sa.Column('created_date', sa.DateTime, nullable=False),
        sa.Column('updated_date', sa.DateTime, nullable=True),
        sa.Column('deleted_date', sa.DateTime, nullable=True)
    )


def downgrade():
    op.drop_table('users')

"""empty message

Revision ID: b7f5b5539aee
Revises: c33ac6a32108
Create Date: 2017-05-19 11:41:26.612621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f5b5539aee'
down_revision = 'c33ac6a32108'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=80),
               nullable=False)
    op.alter_column('users', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('users', 'confirmed_at',
               existing_type=sa.TIMESTAMP(timezone=True),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'confirmed_at',
               existing_type=sa.TIMESTAMP(timezone=True),
               nullable=True)
    op.alter_column('users', 'active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('roles', 'name',
               existing_type=sa.VARCHAR(length=80),
               nullable=True)
    # ### end Alembic commands ###

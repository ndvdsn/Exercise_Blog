"""exercises table

Revision ID: 62c718be5991
Revises: eb8019a24ca0
Create Date: 2020-03-24 19:58:45.379764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62c718be5991'
down_revision = 'eb8019a24ca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('date_time', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=140), nullable=True),
    sa.Column('details', sa.String(length=240), nullable=True),
    sa.Column('contact', sa.String(length=120), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_exercise_timestamp'), 'exercise', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_exercise_timestamp'), table_name='exercise')
    op.drop_table('exercise')
    # ### end Alembic commands ###

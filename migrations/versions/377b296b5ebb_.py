"""empty message

Revision ID: 377b296b5ebb
Revises: 254cb2cbc828
Create Date: 2020-06-02 11:22:45.826596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '377b296b5ebb'
down_revision = '254cb2cbc828'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercisesxblock', sa.Column('block_id', sa.Integer(), nullable=True), schema='lacucha')
    op.add_column('exercisesxblock', sa.Column('exercise_id', sa.Integer(), nullable=True), schema='lacucha')
    op.add_column('exercisesxblock', sa.Column('id_exercisexblock', sa.Integer(), nullable=False), schema='lacucha')
    op.create_unique_constraint(None, 'exercisesxblock', ['id_exercisexblock'], schema='lacucha')
    op.drop_constraint('exercisesxblock_id_exercise_fkey', 'exercisesxblock', schema='lacucha', type_='foreignkey')
    op.drop_constraint('exercisesxblock_id_block_fkey', 'exercisesxblock', schema='lacucha', type_='foreignkey')
    op.create_foreign_key(None, 'exercisesxblock', 'exercises', ['exercise_id'], ['id_exercise'], source_schema='lacucha', referent_schema='lacucha')
    op.create_foreign_key(None, 'exercisesxblock', 'blocks', ['block_id'], ['id_block'], source_schema='lacucha', referent_schema='lacucha')
    op.drop_column('exercisesxblock', 'id_exercise', schema='lacucha')
    op.drop_column('exercisesxblock', 'id_block', schema='lacucha')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercisesxblock', sa.Column('id_block', sa.INTEGER(), autoincrement=False, nullable=False), schema='lacucha')
    op.add_column('exercisesxblock', sa.Column('id_exercise', sa.INTEGER(), autoincrement=False, nullable=False), schema='lacucha')
    op.drop_constraint(None, 'exercisesxblock', schema='lacucha', type_='foreignkey')
    op.drop_constraint(None, 'exercisesxblock', schema='lacucha', type_='foreignkey')
    op.create_foreign_key('exercisesxblock_id_block_fkey', 'exercisesxblock', 'blocks', ['id_block'], ['id_block'], source_schema='lacucha', referent_schema='lacucha')
    op.create_foreign_key('exercisesxblock_id_exercise_fkey', 'exercisesxblock', 'exercises', ['id_exercise'], ['id_exercise'], source_schema='lacucha', referent_schema='lacucha')
    op.drop_constraint(None, 'exercisesxblock', schema='lacucha', type_='unique')
    op.drop_column('exercisesxblock', 'id_exercisexblock', schema='lacucha')
    op.drop_column('exercisesxblock', 'exercise_id', schema='lacucha')
    op.drop_column('exercisesxblock', 'block_id', schema='lacucha')
    # ### end Alembic commands ###
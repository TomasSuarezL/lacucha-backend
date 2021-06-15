"""empty message

Revision ID: 76825e40921e
Revises: c2445fb09781
Create Date: 2021-06-05 22:59:45.782034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76825e40921e'
down_revision = 'c2445fb09781'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ejercicios', sa.Column('peso_inicial', sa.Integer(), nullable=True))
    op.add_column('ejercicios', sa.Column('es_temporal', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ejercicios', 'es_temporal')
    op.drop_column('ejercicios', 'peso_inicial')
    # ### end Alembic commands ###

"""empty message

Revision ID: c2445fb09781
Revises: 0fb76a5bfe67
Create Date: 2021-05-26 19:42:42.852889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2445fb09781'
down_revision = '0fb76a5bfe67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ejerciciosxbloque_id_bloque_fkey', 'ejerciciosxbloque', type_='foreignkey')
    op.create_foreign_key(None, 'ejerciciosxbloque', 'bloques', ['id_bloque'], ['id_bloque'])
    op.add_column('sesiones', sa.Column('num_sesion', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sesiones', 'num_sesion')
    op.drop_constraint(None, 'ejerciciosxbloque', type_='foreignkey')
    op.create_foreign_key('ejerciciosxbloque_id_bloque_fkey', 'ejerciciosxbloque', 'bloques', ['id_bloque'], ['id_bloque'], ondelete='CASCADE')
    # ### end Alembic commands ###

"""empty message

Revision ID: 50f2de518044
Revises: 96053511efb6
Create Date: 2021-06-27 16:42:09.312346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50f2de518044'
down_revision = '96053511efb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'plantillas', ['id_plantilla'])
    op.add_column('sesionesxplantilla', sa.Column('id_sesion', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'sesionesxplantilla', ['id_sesionesxplantilla'])
    op.drop_constraint('sesionesxplantilla_id_ejercicio_fkey', 'sesionesxplantilla', type_='foreignkey')
    op.create_foreign_key(None, 'sesionesxplantilla', 'sesiones', ['id_sesion'], ['id_sesion'])
    op.drop_column('sesionesxplantilla', 'id_ejercicio')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sesionesxplantilla', sa.Column('id_ejercicio', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'sesionesxplantilla', type_='foreignkey')
    op.create_foreign_key('sesionesxplantilla_id_ejercicio_fkey', 'sesionesxplantilla', 'sesiones', ['id_ejercicio'], ['id_sesion'])
    op.drop_constraint(None, 'sesionesxplantilla', type_='unique')
    op.drop_column('sesionesxplantilla', 'id_sesion')
    op.drop_constraint(None, 'plantillas', type_='unique')
    # ### end Alembic commands ###
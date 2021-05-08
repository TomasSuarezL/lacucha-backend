"""empty message

Revision ID: 209e3aba0bc7
Revises: 48f44c2d3a1b
Create Date: 2021-05-03 14:29:40.671006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "209e3aba0bc7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "ejerciciosxbloque_id_bloque_fkey", "ejerciciosxbloque", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "ejerciciosxbloque", "bloques", ["id_bloque"], ["id_bloque"]
    )
    op.drop_constraint("mesociclos_id_usuario_fkey", "mesociclos", type_="foreignkey")
    op.create_foreign_key(
        None, "mesociclos", "usuarios", ["id_usuario"], ["id_usuario"]
    )
    op.add_column("usuarios", sa.Column("rol", sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("usuarios", "rol")
    op.drop_constraint(None, "mesociclos", type_="foreignkey")
    op.create_foreign_key(
        "mesociclos_id_usuario_fkey",
        "mesociclos",
        "usuarios",
        ["id_usuario"],
        ["id_usuario"],
        ondelete="CASCADE",
    )
    op.drop_constraint(None, "ejerciciosxbloque", type_="foreignkey")
    op.create_foreign_key(
        "ejerciciosxbloque_id_bloque_fkey",
        "ejerciciosxbloque",
        "bloques",
        ["id_bloque"],
        ["id_bloque"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###

"""delete outlay_class

Revision ID: 8d7c35336d5e
Revises: dba7b10aa37d
Create Date: 2022-09-15 15:12:58.702839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d7c35336d5e'
down_revision = 'dba7b10aa37d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('directory_of_outlay_class')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('directory_of_outlay_class',
    sa.Column('id_outlay_class', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('outlay_class', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_outlay_class', name='directory_of_outlay_class_pkey')
    )
    # ### end Alembic commands ###

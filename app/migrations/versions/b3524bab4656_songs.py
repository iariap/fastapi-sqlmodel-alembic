"""songs

Revision ID: b3524bab4656
Revises: 
Create Date: 2024-01-04 14:40:14.960359

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel  # NEW


# revision identifiers, used by Alembic.
revision = 'b3524bab4656'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'song',
        sa.Column(
            'id',
            sqlmodel.sql.sqltypes.GUID(),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('current_timestamp(0)'),
            nullable=False,
        ),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            'artist', sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_song_id'), 'song', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_song_id'), table_name='song')
    op.drop_table('song')
    # ### end Alembic commands ###

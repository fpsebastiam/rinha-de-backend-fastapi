"""Create user table

Revision ID: 6a5186e11e8f
Revises: 
Create Date: 2023-09-23 20:14:30.660768

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6a5186e11e8f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('pessoa',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('apelido', sa.String(length=32), nullable=False),
    sa.Column('nascimento', sa.String(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('stack', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_pessoa_apelido'), 'pessoa', ['apelido'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_pessoa_apelido'), table_name='pessoa')
    op.drop_table('pessoa')

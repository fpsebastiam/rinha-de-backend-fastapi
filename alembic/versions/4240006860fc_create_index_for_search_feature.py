"""Create index for search feature

Revision ID: 4240006860fc
Revises: 6a5186e11e8f
Create Date: 2023-09-26 07:53:17.245684

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4240006860fc'
down_revision: Union[str, None] = '6a5186e11e8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION pg_trgm;")

    op.execute("""
        ALTER TABLE pessoa
        ADD COLUMN busca VARCHAR GENERATED ALWAYS AS (
            apelido || ' ' || nome || ' ' || stack
        ) STORED
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_pessoa_busca_gist ON pessoa USING GIST (busca gist_trgm_ops);")


def downgrade() -> None:
    op.drop_index(op.f('idx_pessoa_busca_gist'), table_name='pessoa')
    op.drop_column('pessoa', 'busca')

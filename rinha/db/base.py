# Import all the models, so that Base has them before being
# imported by Alembic
from rinha.db.base_class import Base  # noqa
from rinha.models.pessoa import Pessoa  # noqa

# Import all the models, so that Base has them before being
# imported by Alembic
# from app.src.models.shiny_user import ShinyUser  # noqa
# from app.src.models.discount import Discount  # noqa
# from app.src.models.constr_data import ConstrData  # noqa
# from app.src.models.app_data import AppData  # noqa

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

from app.src.db.base_class import Base  # noqa

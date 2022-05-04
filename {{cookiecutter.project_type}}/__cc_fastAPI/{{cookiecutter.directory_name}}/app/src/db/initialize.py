# Initialize the db with the tables and dummy data
from app.src.logger import logger
from app.src.config import settings
from app.src.models.user import User
from app.src.db.manager import create_tables, insert_data
from app.src.common.security import get_password_hash
from app.src.db.engine import SessionLocal


def initialization() -> bool:
    logger.debug("Starting initialization of DB for first run")
    try:
        create_tables()
        add_user()
        logger.debug("Initialization completed")
        return True
    except Exception as message:
        logger.error(f"Impossible to launch the db initialization: {message}")
        logger.exception(message)
        return False


def add_user() -> None:
    logger.debug("Adding the first admin user")

    admin_user = User(
        name=settings.APP_USER_NAME,
        username=settings.APP_USER_USERNAME,
        surname=settings.APP_USER_SURNAME,
        email=settings.APP_USER_EMAIL,
        password=get_password_hash(settings.APP_USER_PASSWORD),
        token=get_password_hash(settings.APP_USER_TOKEN),
        isAdmin=settings.APP_USER_ISADMIN,
    )
    # check if the user exist
    with SessionLocal.begin() as session:
        existing_user = (
            session.query(User).filter(User.username == admin_user.username).first()
        )

    if existing_user:
        logger.debug("User already existing")
    else:
        # insert the new user if not exist
        insert_data(admin_user)
        logger.debug("First user inserted")


if __name__ == "__main__":
    initialization()

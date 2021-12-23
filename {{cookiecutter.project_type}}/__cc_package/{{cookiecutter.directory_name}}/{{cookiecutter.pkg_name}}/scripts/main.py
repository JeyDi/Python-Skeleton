from {{cookiecutter.pkg_name}}.src.logger import logger
from {{cookiecutter.pkg_name}}.src.config import APP_NAME
from {{cookiecutter.pkg_name}}.src.core.manager import logic_test, convert_numbers

if __name__ == "__main__":
    logger.info(f"Welcome to: {APP_NAME}")

    message = "Ciao JeyDi!"
    numbers = [1, 2, 3, 4, 5, 6]

    new_message = logic_test(message)
    result = convert_numbers(numbers)
    logger.info(f"Message: {new_message}, with numbers: {numbers}")

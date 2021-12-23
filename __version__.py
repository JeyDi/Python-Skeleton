__version__ = "0.0.1"
from typing import Union


def format_unit(value: Union[float, int], unit: str) -> str:
    """[summary]

    Args:
        value (Union[float, int]): [description]
        unit (str): [description]

    Returns:
        str: [description]
    """
    return "{} {}".format(value, unit)

import hashlib
from typing import Optional


def generate_key(
    namespace: Optional[str] = "",
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    """Keybuilder key generator.

    This function allow you to generate a new encoded hash key using namespace, args and kwargs.

    It's mainly use in the cache system, but can be usefull for other purposes.

    You can use the namespace to set a custom property not converted to hash before.

    Be carefull: you cannot come back from hash md5 to the original string value.

    Please set args, kwarg and a namespace to avoid key conflicts

    Args:
        namespace (Optional[str], optional): If you want to save a namespace. Defaults to "".
        args (Optional[tuple], optional): If you want to pass some standard arguments. Defaults to None.
        kwargs (Optional[dict], optional): If you want to pass some key/value arguments to the key. Defaults to None.

    Returns:
        str: The generated key
    """
    # nosec:B303, S303 mypy
    cache_key = namespace + hashlib.md5(f"{args}:{kwargs}".encode()).hexdigest()
    return cache_key

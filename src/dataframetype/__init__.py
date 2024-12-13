import copy
from typing import Any, get_args, get_origin, Generic, TypeVar
from typing import _GenericAlias  # type: ignore[attr-defined]

import pandas as pd

__orig_generic_alias_call = copy.copy(_GenericAlias.__call__)


def __patched_generic_alias_call(self: Any, *args: Any, **kwargs: Any) -> Any:
    """
    Black magic to run validation on initialization.
    `_validate()` can't be called in `__init__` method because `get_args(self.__orig_class__)` won't work properly yet.
    It only works after the `_GenericAlias.__call__`.
    """
    result = __orig_generic_alias_call(self, *args, **kwargs)

    if get_origin(self) is TypeFrame:
        result._validate()

    return result


_GenericAlias.__call__ = __patched_generic_alias_call


P = TypeVar("P", covariant=True)


class TypeFrame(pd.DataFrame, Generic[P]):
    def _validate(self) -> None:
        p_type = get_args(self.__orig_class__)[0]

        for col, expected in p_type.__annotations__.items():
            actual = self[col].dtype

            if actual == expected or isinstance(actual, expected):
                continue

            raise ValueError(
                f"Column '{col}' must have dtype '{expected}'(`{object.__str__(expected)}`) but found '{actual}'(`{object.__str__(actual)}`)"
            )

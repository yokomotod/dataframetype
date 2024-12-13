import unittest
from typing import Protocol
import numpy as np
import pandas as pd
from dataframetype import TypeFrame


class TestDataFrameType(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame(
            {
                "i1": pd.Series([1, 2, 3], dtype=np.int64),
                "i2": pd.Series([1, 2, 3], dtype=pd.Int64Dtype()),
                "s1": pd.Series(["a", "b", "c"]),
                "s2": pd.Series(["a", "b", "c"], dtype=pd.StringDtype()),
            }
        )

    def test_validation_ok(self) -> None:
        class MyScheme(Protocol):
            i1: np.int64
            i2: pd.Int64Dtype
            s1: object
            s2: pd.StringDtype

        TypeFrame[MyScheme](self.df)

    def test_validation_fail(self) -> None:
        class MyScheme(Protocol):
            i1: np.int64
            i2: pd.Int64Dtype
            s1: object
            s2: np.float64

        with self.assertRaises(ValueError):
            TypeFrame[MyScheme](self.df)

    def test_mypy(self) -> None:
        """
        This test is for mypy type checking.
        `# type: ignore` means that it should raise an error.
        If it doesn't raise an error, mypy will raise `Invalid "type: ignore" comment` error
        since `--warn-unused-ignores` is enabled with `--strict` option.
        """

        class MyScheme(Protocol):
            i1: np.int64
            s1: object

        # should accept MyScheme
        class SubScheme(Protocol):
            i1: np.int64

        # should not accept MyScheme

        class OtherScheme(Protocol):
            f1: np.float64

        df = TypeFrame[MyScheme](self.df)

        _df2: TypeFrame[SubScheme] = df
        _df3: TypeFrame[OtherScheme] = df  # type: ignore

        def funcA(df: TypeFrame[SubScheme]) -> None:
            pass

        def funcB(df: TypeFrame[OtherScheme]) -> None:
            pass

        funcA(df)
        funcB(df)  # type: ignore


if __name__ == "__main__":
    unittest.main()

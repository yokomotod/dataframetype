from typing import Protocol

import numpy as np
import pandas as pd
import pandera as pa

from pandera.typing import DataFrame, Series
from dataframetype import TypeFrame


class Schema(pa.DataFrameModel):
    state: Series[str]
    city: Series[str]
    price: Series[int] = pa.Field(in_range={"min_value": 5, "max_value": 20})


class Schema2(pa.DataFrameModel):
    state: Series[str]
    city: Series[str]


pf = DataFrame[Schema](
    {
        "state": ["NY", "FL", "GA", "CA"],
        "city": ["New York", "Miami", "Atlanta", "San Francisco"],
        "price": [8, 12, 10, 16],
    }
)

pf2: DataFrame[Schema2] = pf


def pfunc(pf: DataFrame[Schema2]) -> None:
    print(pf)


pfunc(pf)


class MyScheme(Protocol):
    i1: np.int64
    i2: pd.Int64Dtype
    s1: object
    s2: pd.StringDtype


class MyScheme2(Protocol):
    i1: np.int64
    s1: object
    # f1: np.float64


df = TypeFrame[MyScheme](
    {
        "i1": pd.Series([1, 2, 3], dtype=np.int64),
        "i2": pd.Series([1, 2, 3], dtype=pd.Int64Dtype()),
        "s1": pd.Series(["a", "b", "c"]),
        "s2": pd.Series(["a", "b", "c"], dtype=pd.StringDtype()),
    }
)

df2: TypeFrame[MyScheme2] = df


def func(df: TypeFrame[MyScheme2]) -> None:
    print(df)


func(df)


def main():
    print("Hello from example!")


if __name__ == "__main__":
    main()

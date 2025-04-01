import pandas as pd
import numpy as np
import mplfinance as mf

def load_data(path: str, sep: str = "\t", nrows: int = 1000000) -> pd.DataFrame:
    return pd.read_csv(path, sep=sep, nrows=nrows)

def get_duplicated_indices(data: pd.DataFrame) -> list[int]:
    duplicated = data[data.duplicated(subset=["<DATE>", "<TIME>"], keep=False)]
    duplicated_with_nan = duplicated[
        duplicated["<BID>"].isna() | duplicated["<ASK>"].isna()
    ]
    return duplicated_with_nan.index.to_list()

def remove_duplicated_rows(data: pd.DataFrame, indices: list[int]) -> pd.DataFrame:
    return data.drop(index=indices)

def add_spread_column(data: pd.DataFrame) -> pd.DataFrame:
    data["<ASK>"] = data["<ASK>"].fillna(0)
    data["<BID>"] = data["<BID>"].fillna(0)
    data["<SPREAD>"] = data["<ASK>"] - data["<BID>"]
    return data

def fill_missing_ask_bid(data: pd.DataFrame) -> pd.DataFrame:
    data["<BID>"] = np.where(
        data["<BID>"] == 0,
        data["<ASK>"] - data["<SPREAD>"].shift(1),
        data["<BID>"]
    )
    data["<ASK>"] = np.where(
        data["<ASK>"] == 0,
        data["<BID>"] + data["<SPREAD>"].shift(1),
        data["<ASK>"]
    )
    return data

def create_candlestick_plot(data: pd.DataFrame):
    ohlc = data["<BID>"].resample("1min").ohlc() 
    mf.plot(ohlc, type='candle', style='charles', title="Gráfico de velas - BID", ylabel="Precio BID")

def save_data(data: pd.DataFrame, output_path: str):
    data.to_csv(output_path, index=False)


def main(input_path: str, output_path: str):
    raw_data = load_data(input_path)
    duplicate_indices = get_duplicated_indices(raw_data)
    clean_data = remove_duplicated_rows(raw_data, duplicate_indices)
    with_spread = add_spread_column(clean_data)
    completed_data = fill_missing_ask_bid(with_spread)
    #create_candlestick_plot(completed_data)
    print(completed_data)
    save_data(completed_data, output_path)

if __name__ == "__main__":
    main("resources/task.csv", "task.csv")

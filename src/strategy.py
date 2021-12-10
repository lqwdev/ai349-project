import pandas as pd
import ta


def bh(data: pd.DataFrame, start: int = -1402, end: int = -1) -> pd.DataFrame:
    bh_data = data.copy(deep=True)
    bh_data['action'] = bh_data.apply(lambda _: 'H', axis=1)
    bh_data = bh_data[start:end]
    bh_data.loc[bh_data.index[0], 'action'] = 'B'
    return bh_data


def macd(data: pd.DataFrame, start: int = -1402, end: int = -1) -> pd.DataFrame:
    def macd_cross(row):
        if row['trend_macd_diff_shifted'] > 0 and row['trend_macd_diff'] < 0:
            return 'B'
        if row['trend_macd_diff_shifted'] < 0 and row['trend_macd_diff'] > 0:
            return 'S'
        return 'H'

    macd_data = ta.utils.dropna(data)
    macd_data = ta.add_all_ta_features(macd_data, "Open", "High", "Low", "Close", "Volume", fillna=True)
    macd_data = macd_data[["Open", "High", "Low", "Close", "Volume", 'trend_macd_diff', 'trend_macd', 'trend_macd_signal']]

    macd_data['trend_macd_diff_shifted'] = macd_data['trend_macd_diff'].shift(-1)
    macd_data['cross'] = macd_data.apply(lambda row: macd_cross(row), axis=1)
    macd_data['action'] = macd_data['cross'].shift(1)
    macd_data = macd_data[start:end][["Open", "High", "Low", "Close", "Volume", "action"]]
    return macd_data

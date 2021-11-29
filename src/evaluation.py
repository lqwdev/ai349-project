import pandas as pd

def eval(df: pd.DataFrame, original: int = 10000) -> pd.DataFrame:
    cash, shares = original, 0
    endprice, values = None, []
    
    for _, row in df.iterrows():
        price, endprice = row['Open'], row['Close']
        action = row['action']

        if action == 'B' and cash > 0:
            buy = cash / price
            cash -= buy * price
            shares += buy
        elif action == 'S' and shares > 0:
            sell = shares
            cash += sell * price
            shares -= sell
        
        values.append(cash + shares * endprice)
    
    value = cash + endprice * shares
    print(f"Performance: {round(100 * (value - original) / original, 2)}%")

    perf = pd.DataFrame(index=df.index)
    perf['value'] = values
    perf['percentage'] = 100 * (perf['value'] - original) / original
    return perf

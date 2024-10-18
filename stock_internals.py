import yfinance as yf
import numpy as np
import pandas as pd


def count_trend_after_direction_change(stock_data, n, trend_up=True, direction=False):

    stock_data = stock_data.sort_index()

    close_prices = stock_data.values
    count = 0
    i = 1  

    while i < len(close_prices) - n:
        
        if (close_prices[i] > close_prices[i - 1] if direction else close_prices[i] < close_prices[i - 1]):

            streak_valid = True

            for j in range(i + 1, i + 1 + n):

                if (close_prices[j] <= close_prices[j - 1] if trend_up else close_prices[j] >= close_prices[j - 1]):

                    streak_valid = False

                    break

            if streak_valid:

                count += 1
                i += n

            else:

                i += 1
                
        else:

            i += 1

    return count


def get_df_given_inputs(n, start_date, end_date, stock_tickers):
    data = yf.download(stock_tickers, start=start_date, end=end_date)['Close']
    data.index = pd.to_datetime(data.index)

    results = []
    for column in data.columns:
        up_down = count_trend_after_direction_change(data[column], n, trend_up=False, direction=True)
        up_up = count_trend_after_direction_change(data[column], n, trend_up=True, direction=True)
        pup = 0
        if (up_up + up_down) > 0:
            pup = up_up/(up_up + up_down)
        else:
            pup = 0
        down_down = count_trend_after_direction_change(data[column], n, trend_up=False, direction=False)
        down_up = count_trend_after_direction_change(data[column], n, trend_up=True, direction=False)
        pdown = 0
        if (down_down + down_up) > 0:
            pdown = down_up/(down_down + down_up)
        else:
            pdown = 0

        results.append({
            'Ticker': column,
            'Up-Down': up_down,
            'Up-Up': up_up,
            'P(Up|Up)': pup,
            'Down-Down': down_down,
            'Down-Up': down_up,
            'P(Up|Down)': pdown
        })

    result_df = pd.DataFrame(results)

    return result_df


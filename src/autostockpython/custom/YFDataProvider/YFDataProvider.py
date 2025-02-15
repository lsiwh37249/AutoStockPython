from abc import ABC, abstractmethod
from autostockpython.module.DataProvider import DataProvider
import yfinance as yf
import json
from numpyencoder import NumpyEncoder

class YFDataProvider(DataProvider):
    def __init__(self):
        super().__init__()

    def get_info(self, ticker_symbol):
        #티커 객체 생성
        ticket = yf.Ticker(ticker_symbol)

        hist = ticket.history(period="1d")

        if not hist.empty:
            date_time = hist.index[0]
            opening_price = hist['Open'].iloc[0]
            high_price = hist['High'].iloc[0]
            low_price = hist['Low'].iloc[0]
            closing_price = hist['Close'].iloc[0]
            volume = hist['Volume'].iloc[0]
            
            # JSON 데이터 생성
            json_data = {
                "market": ticker_symbol,
                "date_time": date_time.isoformat(),
                "opening_price": opening_price,
                "high_price": high_price,
                "low_price": low_price,
                "closing_price": closing_price,
                "acc_price": closing_price * volume,
                "acc_volume": volume
            }
            return json.dumps(json_data, indent=2, cls=NumpyEncoder)
        else:
            return "데이터를 가져올 수 없습니다."

    def get_price(self, ticker_symbol):
        try:
            ticker = yf.Ticker(ticker_symbol)
            latest_price = ticker.fast_info.last_price
            print(f"{ticker_symbol}의 최신 주가: ${latest_price:.2f}")
            return latest_price
        except AttributeError:
            print(f"{ticker_symbol}의 정보를 가져오는 데 실패했습니다.")
            return None

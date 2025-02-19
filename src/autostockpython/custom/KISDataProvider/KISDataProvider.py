from abc import ABC, abstractmethod
from autostockpython.module.DataProvider import DataProvider
from datetime import datetime
import requests
import json
import os
import pandas as pd

class KISDataProvider(DataProvider):
    def __init__(self):
        super().__init__()
        # 추가적인 초기화 코드
        self.appKey = os.getenv("APPKEY")
        self.appSecret = os.getenv("SECRETKEY")
        self.grant_type = "client_credentials"
        self.VTS = "https://openapi.koreainvestment.com:9443"
        self.access_token = ""
    def get_Token(self):
        # 데이터를 로드하는 메소드
        url = f"{self.VTS}/oauth2/tokenP"

        payload = json.dumps({
          "grant_type": self.grant_type,
          "appkey": self.appKey,
          "appsecret": self.appSecret
        })
        headers = {
          'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json().get("access_token")
        self.access_token = token
        return 0

    def get_info(self, mrkt, ticker):
            
        url = f"{self.VTS}/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code={mrkt}&fid_input_iscd={ticker}"

        payload = ""
        headers = {
          'content-type': 'application/json',
          'authorization': f"Bearer {self.access_token}",
          'appkey': self.appKey,
          'appSecret': self.appSecret,
          'tr_id': 'FHKST01010100'
    }
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json().get("output")
        market = data.get("rprs_mrkt_kor_name")
        date_time = datetime.now()
        opening_price = data.get("stck_oprc")
        high_price = data.get("stck_hgpr")
        low_price = data.get("stck_lwpr")
        closing_price = data.get("stck_prpr")  # 수정된 부분
        acc_price = data.get("acml_tr_pbmn")
        acc_volume = data.get("acml_vol")
        # JSON 형식으로 변환
        json_data = {
            "market": market,
            "date_time": date_time.isoformat(),
            "opening_price": opening_price,
            "high_price": high_price,
            "low_price": low_price,
            "closing_price": closing_price,
            "acc_price": acc_price,
            "acc_volume": acc_volume
        }

        json_string = json.dumps(json_data, ensure_ascii=False, indent=2)
        return json_string


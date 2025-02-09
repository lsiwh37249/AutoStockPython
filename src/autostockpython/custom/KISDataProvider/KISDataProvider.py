from abc import ABC, abstractmethod
from autostockpython.module.DataProvider import DataProvider

class KISDataProvider(DataProvider):
    def __init__(self):
        super().__init__()
        # 추가적인 초기화 코드
        self.appKey = ""
        self.appSecret = ""
        self.accountInfo = ""

    def get_info(self):
        # DataProvider의 추상 메소드 구현
        
        pass

    def load_data(self):
        # 데이터를 로드하는 메소드
        print("load_data")
        pass

    def update_data(self):
        # 데이터를 업데이트하는 메소드
        print("update_data")
        pass

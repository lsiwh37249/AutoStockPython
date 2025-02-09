from abc import ABC, abstractmethod
from autostockpython.module.DataProvider import DataProvider

class MyFirstDataProvider(DataProvider):
    def __init__(self):
        super().__init__()
        # 추가적인 초기화 코드
        pass

    def get_info(self):
        # DataProvider의 추상 메소드 구현
        # 실제 데이터를 가져오는 로직을 여기에 구현
        
        pass

    def load_data(self):
        # 데이터를 로드하는 메소드
        pass

    def update_data(self):
        # 데이터를 업데이트하는 메소드
        pass

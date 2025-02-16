from autostockpython import *
from abc import ABC, abstractmethod
import logging

class Strategy(ABC):
    """
    데이터 소스로부터 데이터를 수집해서 정보를 제공하는 클래스
    """

    def __init__(self, budget, min_price=5000):
        self.data = [] # 거래 데이터 리스트
        self.result = [] # 거래 요청 결과 리스트
        self.request = [] # 마지막 거래 요청
        self.budget = budget
        self.balance = budget
        self.min_price = min_price
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def update_trading_info(self):
        """
        거래 정보를 업데이트하는 메서드
        """
        pass

    @abstractmethod
    def get_request(self):
        """
        거래 요청을 생성하는 메서드
        :return: 거래 요청 정보를 담은 딕셔너리
        """
        pass

    @abstractmethod
    def update_result(self):
        """
        거래 결과를 업데이트하는 메서드
        :param result: 거래 결과 정보를 담은 딕셔너리
        """

        pass

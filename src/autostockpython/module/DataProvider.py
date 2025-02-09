from AutoStockPython import *

class DataProvider():
    """
    데이터 소스로부터 데이터를 수집해서 정보를 제공하는 클래스
    """

    @abstractmethod
    def get_info(self):
        """
        현재 거래 정보를 딕셔너리로 전달

        Returns: 거래 정보 딕셔너리
        {
            "market": 거래 시장 종류
            "date_time": 정보의 기준 시간
            "opening_price": 시작 거래 가격
            "high_price": 최고 거래 가격
            "low_price": 최저 거래 가격
            "closing_price": 마지막 거래 가격
            "acc_price": 단위 시간 내 누적 거래 금액
            "acc_volume": 단위 시간 내 누적 거래 양

        }
        """

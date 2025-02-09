class BaseTrading:
    def __init__(self):
        pass

    def get_price_data(self):
        # 가격 데이터를 가져오는 로직
        pass

    def place_order(self):
        # 매수/매도 주문을 실행하는 로직
        pass

    def main(self):
        # 메인 실행 로직
        self.get_price_data()
        self.moving_average_strategy()
        self.place_order()
        pass

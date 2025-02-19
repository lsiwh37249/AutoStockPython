import copy

import logging
from datetime import datetime, timedelta
import time

class StrategyBuyAndHold():
    def __init__(self, budget, min_price=5000):
        self.data = [] # 거래 데이터 리스트
        self.result = [] # 거래 요청 결과 리스트
        self.request = [] # 마지막 거래 요청
        self.waiting_requests = []
        self.budget = budget # 예산
        self.balance = budget # 남은 금액
        self.min_price = min_price
        self.is_simulation = False
        self.COMMISSION_RATIO  = 0.007
        self.logger = logging.getLogger(__name__)

    def update_trading_info(self, info):
        """
        거래 정보를 업데이트하는 메서드
        """
        self.data.append(copy.deepcopy(info))
        return info

    def get_request(self):
        """
        거래 요청을 생성하는 메서드
        투자 전략 : 초기 투자금의 1/5만큼씩 매수하는 전략
        :return: 거래 요청 정보를 담은 딕셔너리
        """
        if len(self.data) == 0 or self.data[-1] is None:
            raise UserWarning("data is empty")

        last_closing_price = self.data[-1]["closing_price"]
        now = datetime.now().strftime("%Y-%m-%d")

        if self.is_simulation:
            now = self.data[-1]["date_time"]

        target_budget = self.budget / 5
        if target_budget > self.balance:
            target_budget = self.balance

        amount = round(target_budget / last_closing_price, 4)
        trading_request = {
            "id" : str(round(time.time(), 3)),
            "type" : "buy",
            "price" : last_closing_price,
            "amount" : amount,
            "date_time" : now,
        }
        total_value = round(float(last_closing_price) * amount)

        if self.min_price > total_value or total_value > self.balance:
            raise UserWarning("total_value or balance is too small")

        self.logger.info(f"[REQ] id : {trading_request['id']}")
        self.logger.info(f"=====================")
        self.logger.info(f"price: {last_closing_price}, amount: {amount}")
        self.logger.info(f"type: buy, total_value: {total_value}")
        self.logger.info(f"=====================")

        final_requests = []
        for request_id in self.waiting_requests:
            self.logger.info(f"cancel request added! {request_id}")
            final_requests.append(
                {
                    "id" : request_id,
                    "type" : "cancel",
                    "price" : 0,
                    "amount" : 0,
                    "date_time" : now,
                }
            )
        final_requests.append(trading_request)
        return final_requests

    def update_result(self, result):
        """
        요청한 거래 결과를 업데이트하는 메서드
        request : 거래 요청 정보
        result:
        {
            "request" : 요청 정보,
            "type" : 거래 유형 sell, buy, cancel,
            "price" : 거래 가격,
            "amount" : 거래 수량,
            "msg" : 거래 결과 메시지,
            "state" : 거래 상태 requested, done,
            "date_time" : 시뮬레이션 모드에서는 데이터 시간 +2초
        }
        """

        request = result["request"]
        if result["state"] == "requested":
            self.waiting_requests[request["id"]] = result
            return

        if result["state"] == "done" and request["id"] in self.waiting_requests:
            del self.waiting_requests[request["id"]]

        total = float(result["price"]) * float(result["amount"])
        fee = total * self.COMMISSION_RATIO
        if result["type"] == "buy":
            self.balance -= round(total + fee)
        else:
            self.balance += round(total - fee)

        self.logger.info(f"[RESULT] id : {result['request']['id']}")
        self.logger.info(f"==================")
        self.logger.info(f"type: {result['type']}, msg: {result['msg']}")
        self.logger.info(f"price: {result['price']}, amount: {result['amount']}")
        self.logger.info(f"total: {total}, balace: {self.balance}")
        self.logger.info(f"==================")
        self.result.append(copy.deepcopy(result))

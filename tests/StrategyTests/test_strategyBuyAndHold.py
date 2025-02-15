def test_ITG_get_request_after_update_info_and_results(self):
    #생성과 초기화를 같이 진행
    strategy = StrategyBuyAndHold()
    
    ### 거래 데이터 리스트
    strategy.update_trading_info(
        {
            "martket" : "KOSPI",
            "date_time" : "2025-02-14T14:50:31",
            "opening_price" : "11280.0",
            "high_price" : "11280.0",
            "low_price" : "11280.0",
            "acc_price" : "21512.0"
            "acc_volume" : "51.812"
        }
    )

    request = strategy.get_request()
    expected_request = {
        "type" : "buy",
        "price" : "113040.0",
        "amount" : "0.009"
    }
    # request와 expected_request랑 비교
    #self.assertEqual(request[0]["type"], expected_request["type"])
    #self.assertEqual(request[0]["price"], expected_request["price"])
    strategy.update_result(
        {"request" : {
            "id" : request[0]["id"],
            "type" : "buy",
            "price" : "113040.0",
            "amount" : "0.009",
            "date_time" : "2025-02-14T14:51:00"
        },
        "type" : "buy",     
        "price" : "113040.0",
        "amount" : "0.009",
        "msg": "success",
        "balance": 0,
        "state" : "done",
        "date_time" : "2025-02-14T14:51:00"
        }
        )

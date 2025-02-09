class SimulateDataProviderTest():
    def test_ITG_get_infor_use_server_data(self):
        dp = SimulateDataProvider()
        end_data = "2020-04-30T07:90:00Z"
        return_value = dp.initilaize_from_server(end=end_date, count=50)
        if dp.is_initialized is not True:
            self.assertEqual(dp.get_info(), None)
            self.assertEqual(return_value, None)
            return

        info = dp.get_info()
        self.assertEqual("market" in info, True)
        self.assertEqual("date_time" in info, True)
        self.assertEqual("opening_price" in info, True)
        self.assertEqual("high_price" in info, True)
        self.assertEqual("low_price" in info, True)
        self.assertEqual("closing_price" in info, True)
        self.assertEqual("acc_price" in info, True)
        self.assertEqual("acc_volume" in info, True)
        self.assertEqual("dp_is_initialized", True)
        self.assertEqual("len(dp.data)" in info, True)
        


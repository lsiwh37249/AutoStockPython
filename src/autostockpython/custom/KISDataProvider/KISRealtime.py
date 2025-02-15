# -*- coding: utf-8 -*-
### 모듈 임포트 ###
import os
import sys
import json
import time
import requests
import asyncio
import traceback
import websockets

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

key_bytes = 32


### 함수 정의 ###

# AES256 DECODE
def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))


# 웹소켓 접속키 발급
def get_approval(key, secret):
    # url = https://openapivts.koreainvestment.com:29443' # 모의투자계좌     
    url = 'https://openapi.koreainvestment.com:9443' # 실전투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    time.sleep(0.05)
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key

### 1-1. 국내주식 ###

# 국내주식호가 출력라이브러리
def stockhoka_domestic(data):
    """ 넘겨받는데이터가 정상인지 확인
    print("stockhoka[%s]"%(data))
    """
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("유가증권 단축 종목코드 [" + recvvalue[0] + "]")
    print("영업시간 [" + recvvalue[1] + "]" + "시간구분코드 [" + recvvalue[2] + "]")
    print("======================================")
    print("매도호가10 [%s]    잔량10 [%s]" % (recvvalue[12], recvvalue[32]))
    print("매도호가09 [%s]    잔량09 [%s]" % (recvvalue[11], recvvalue[31]))
    print("매도호가08 [%s]    잔량08 [%s]" % (recvvalue[10], recvvalue[30]))
    print("매도호가07 [%s]    잔량07 [%s]" % (recvvalue[9], recvvalue[29]))
    print("매도호가06 [%s]    잔량06 [%s]" % (recvvalue[8], recvvalue[28]))
    print("매도호가05 [%s]    잔량05 [%s]" % (recvvalue[7], recvvalue[27]))
    print("매도호가04 [%s]    잔량04 [%s]" % (recvvalue[6], recvvalue[26]))
    print("매도호가03 [%s]    잔량03 [%s]" % (recvvalue[5], recvvalue[25]))
    print("매도호가02 [%s]    잔량02 [%s]" % (recvvalue[4], recvvalue[24]))
    print("매도호가01 [%s]    잔량01 [%s]" % (recvvalue[3], recvvalue[23]))
    print("--------------------------------------")
    print("매수호가01 [%s]    잔량01 [%s]" % (recvvalue[13], recvvalue[33]))
    print("매수호가02 [%s]    잔량02 [%s]" % (recvvalue[14], recvvalue[34]))
    print("매수호가03 [%s]    잔량03 [%s]" % (recvvalue[15], recvvalue[35]))
    print("매수호가04 [%s]    잔량04 [%s]" % (recvvalue[16], recvvalue[36]))
    print("매수호가05 [%s]    잔량05 [%s]" % (recvvalue[17], recvvalue[37]))
    print("매수호가06 [%s]    잔량06 [%s]" % (recvvalue[18], recvvalue[38]))
    print("매수호가07 [%s]    잔량07 [%s]" % (recvvalue[19], recvvalue[39]))
    print("매수호가08 [%s]    잔량08 [%s]" % (recvvalue[20], recvvalue[40]))
    print("매수호가09 [%s]    잔량09 [%s]" % (recvvalue[21], recvvalue[41]))
    print("매수호가10 [%s]    잔량10 [%s]" % (recvvalue[22], recvvalue[42]))
    print("======================================")
    print("총매도호가 잔량        [%s]" % (recvvalue[43]))
    print("총매도호가 잔량 증감   [%s]" % (recvvalue[54]))
    print("총매수호가 잔량        [%s]" % (recvvalue[44]))
    print("총매수호가 잔량 증감   [%s]" % (recvvalue[55]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[45]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[46]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[56]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[57]))
    print("예상 체결가            [%s]" % (recvvalue[47]))
    print("예상 체결량            [%s]" % (recvvalue[48]))
    print("예상 거래량            [%s]" % (recvvalue[49]))
    print("예상체결 대비          [%s]" % (recvvalue[50]))
    print("부호                   [%s]" % (recvvalue[51]))
    print("예상체결 전일대비율    [%s]" % (recvvalue[52]))
    print("누적거래량             [%s]" % (recvvalue[53]))
    print("주식매매 구분코드      [%s]" % (recvvalue[58]))
    return recvvalue
    
# 국내주식체결처리 출력라이브러리
def stockspurchase_domestic(data_cnt, data):
    print("============================================")
    menulist = "유가증권단축종목코드|주식체결시간|주식현재가|전일대비부호|전일대비|전일대비율|가중평균주식가격|주식시가|주식최고가|주식최저가|매도호가1|매수호가1|체결거래량|누적거래량|누적거래대금|매도체결건수|매수체결건수|순매수체결건수|체결강도|총매도수량|총매수수량|체결구분|매수비율|전일거래량대비등락율|시가시간|시가대비구분|시가대비|최고가시간|고가대비구분|고가대비|최저가시간|저가대비구분|저가대비|영업일자|신장운영구분코드|거래정지여부|매도호가잔량|매수호가잔량|총매도호가잔량|총매수호가잔량|거래량회전율|전일동시간누적거래량|전일동시간누적거래량비율|시간구분코드|임의종료구분코드|정적VI발동기준가"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1

            
# 국내주식예상체결 출력라이브러리
def stockexppurchase_domestic(data_cnt, data):
    print("============================================")
    menulist = "유가증권단축종목코드|주식체결시간|주식현재가|전일대비구분|전일대비|등락율|가중평균주식가격|시가|고가|저가|매도호가|매수호가|거래량|누적거래량|누적거래대금|매도체결건수|매수체결건수|순매수체결건수|체결강도|총매도수량|총매수수량|체결구분|매수비율|전일거래량대비등락율|시가시간|시가대비구분|시가대비|최고가시간|고가대비구분|고가대비|최저가시간|저가대비구분|저가대비|영업일자|신장운영구분코드|거래정지여부|매도호가잔량1|매수호가잔량1|총매도호가잔량|총매수호가잔량|거래량회전율|전일동시간누적거래량|전일동시간누적거래량비율|시간구분코드|임의종료구분코드"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1

            
# 국내주식체결통보 출력라이브러리
def stocksigningnotice_domestic(data, key, iv):
    
    # AES256 처리 단계
    aes_dec_str = aes_cbc_base64_dec(key, iv, data)
    pValue = aes_dec_str.split('^')

    if pValue[13] == '2': # 체결통보
        print("#### 국내주식 체결 통보 ####")
        menulist = "고객ID|계좌번호|주문번호|원주문번호|매도매수구분|정정구분|주문종류|주문조건|주식단축종목코드|체결수량|체결단가|주식체결시간|거부여부|체결여부|접수여부|지점번호|주문수량|계좌명|체결종목명|신용구분|신용대출일자|체결종목명40|주문가격"
        menustr1 = menulist.split('|')
    else:
        print("#### 국내주식 주문·정정·취소·거부 접수 통보 ####")
        menulist = "고객ID|계좌번호|주문번호|원주문번호|매도매수구분|정정구분|주문종류|주문조건|주식단축종목코드|주문수량|주문가격|주식체결시간|거부여부|체결여부|접수여부|지점번호|주문수량|계좌명|주문종목명|신용구분|신용대출일자|체결종목명40|체결단가"
        menustr1 = menulist.split('|')
    
    i = 0
    for menu in menustr1:
        print("%s  [%s]" % (menu, pValue[i]))
        i += 1

# 국내주식 실시간회원사 출력라이브러리
def stocksmember_domestic(data_cnt, data):
    print("============================================")
    print(data)
    menulist = "유가증권단축종목코드|매도2회원사명1|매도2회원사명2|매도2회원사명3|매도2회원사명4|매도2회원사명5|매수회원사명1|매수회원사명2|매수회원사명3|매수회원사명4|매수회원사명5|총매도수량1|총매도수량2|총매도수량3|총매도수량4|총매도수량5|총매수2수량1|총매수2수량2|총매수2수량3|총매수2수량4|총매수2수량5|매도거래원구분1|매도거래원구분2|매도거래원구분3|매도거래원구분4|매도거래원구분5|매수거래원구분1|매수거래원구분2|매수거래원구분3|매수거래원구분4|매수거래원구분5|매도거래원코드1|매도거래원코드2|매도거래원코드3|매도거래원코드4|매도거래원코드5|매수거래원코드1|매수거래원코드2|매수거래원코드3|매수거래원코드4|매수거래원코드5|매도회원사비중1|매도회원사비중2|매도회원사비중3|매도회원사비중4|매도회원사비중5|매수2회원사비중1|매수2회원사비중2|매수2회원사비중3|매수2회원사비중4|매수2회원사비중5|매도수량증감1|매도수량증감2|매도수량증감3|매도수량증감4|매도수량증감5|매수2수량증감1|매수2수량증감2|매수2수량증감3|매수2수량증감4|매수2수량증감5|외국계총매도수량|외국계총매수2수량|외국계총매도수량증감|외국계총매수2수량증감|외국계순매수수량|외국계매도비중|외국계매수2비중|매도2영문회원사명1|매도2영문회원사명2|매도2영문회원사명3|매도2영문회원사명4|매도2영문회원사명5|매수영문회원사명1|매수영문회원사명2|매수영문회원사명3|매수영문회원사명4|매수영문회원사명5"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1              
            
            
# 국내주식 실시간프로그램매매 출력라이브러리
def stocksprogramtrade_domestic(data_cnt, data):
    print("============================================")
    menulist = "유가증권단축종목코드|주식체결시간|매도체결량|매도거래대금|매수2체결량|매수2거래대금|순매수체결량|순매수거래대금|매도호가잔량|매수호가잔량|전체순매수호가잔량"
    menustr = menulist.split('|')
    pValue = data.split('^')
    i = 0
    for cnt in range(data_cnt):  # 넘겨받은 체결데이터 개수만큼 print 한다
        print("### [%d / %d]" % (cnt + 1, data_cnt))
        for menu in menustr:
            print("%-13s[%s]" % (menu, pValue[i]))
            i += 1
            
            
### 2. 해외주식 ###
            
          
# 해외주식(미국)호가 출력라이브러리
def stockhoka_overseas_usa(data):
    """ 넘겨받는데이터가 정상인지 확인
    print("stockhoka[%s]"%(data))
    """
    print(data)
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("실시간종목코드 [" + recvvalue[0] + "]" + ", 종목코드 [" + recvvalue[1] + "]")
    print("소숫점자리수 [" + recvvalue[2] + "]")
    print("현지일자 [" + recvvalue[3] + "]" + ", 현지시간 [" + recvvalue[4] + "]")
    print("한국일자 [" + recvvalue[5] + "]" + ", 한국시간 [" + recvvalue[6] + "]")
    print("======================================")    
    print("매도호가10 [%s]    잔량10 [%s]" % (recvvalue[66], recvvalue[68]))
    print("매도호가09 [%s]    잔량09 [%s]" % (recvvalue[60], recvvalue[62]))
    print("매도호가08 [%s]    잔량08 [%s]" % (recvvalue[54], recvvalue[56]))
    print("매도호가07 [%s]    잔량07 [%s]" % (recvvalue[48], recvvalue[50]))
    print("매도호가06 [%s]    잔량06 [%s]" % (recvvalue[42], recvvalue[44]))
    print("매도호가05 [%s]    잔량05 [%s]" % (recvvalue[36], recvvalue[38]))
    print("매도호가04 [%s]    잔량04 [%s]" % (recvvalue[30], recvvalue[32]))
    print("매도호가03 [%s]    잔량03 [%s]" % (recvvalue[24], recvvalue[26]))
    print("매도호가02 [%s]    잔량02 [%s]" % (recvvalue[18], recvvalue[20]))
    print("매도호가01 [%s]    잔량01 [%s]" % (recvvalue[12], recvvalue[14]))
    print("--------------------------------------")
    print("매수호가01 [%s]    잔량01 [%s]" % (recvvalue[11], recvvalue[13]))
    print("매수호가02 [%s]    잔량02 [%s]" % (recvvalue[17], recvvalue[19]))
    print("매수호가03 [%s]    잔량03 [%s]" % (recvvalue[23], recvvalue[25]))
    print("매수호가04 [%s]    잔량04 [%s]" % (recvvalue[29], recvvalue[31]))
    print("매수호가05 [%s]    잔량05 [%s]" % (recvvalue[35], recvvalue[37]))
    print("매수호가06 [%s]    잔량06 [%s]" % (recvvalue[41], recvvalue[43]))
    print("매수호가07 [%s]    잔량07 [%s]" % (recvvalue[47], recvvalue[49]))
    print("매수호가08 [%s]    잔량08 [%s]" % (recvvalue[53], recvvalue[55]))
    print("매수호가09 [%s]    잔량09 [%s]" % (recvvalue[59], recvvalue[61]))
    print("매수호가10 [%s]    잔량10 [%s]" % (recvvalue[65], recvvalue[67]))
    print("======================================")
    print("매수총 잔량        [%s]" % (recvvalue[7]))
    print("매수총잔량대비      [%s]" % (recvvalue[9]))
    print("매도총 잔량        [%s]" % (recvvalue[8]))
    print("매도총잔략대비      [%s]" % (recvvalue[10]))

async def connect():
    try:
        g_appkey = os.getenv("APPKEY")
        g_appsecret = os.getenv("SECRETKEY")
        g_approval_key= get_approval(g_appkey, g_appsecret)
        print("approval_key [%s]" % (g_approval_key))

        # url = 'ws://ops.koreainvestment.com:31000' # 모의투자계좌
        url = 'ws://ops.koreainvestment.com:21000' # 실전투자계좌

        # 원하는 호출을 [tr_type, tr_id, tr_key] 순서대로 리스트 만들기

        ### 1-1. 국내주식 호가, 체결가, 예상체결, 체결통보 ### # 모의투자 국내주식 체결통보: H0STCNI9
        #code_list = [['1','H0STASP0','005930'],['1','H0STCNT0','005930'],['1', 'H0STANC0', '005930'],['1','H0STCNI0','1069149']]
        code_list = [['1','H0STASP0','005930']]
        ### 1-2. 국내주식 실시간회원사, 실시간프로그램매매, 장운영정보 ###
        # code_list = [['1', 'H0STMBC0', '005930'], ['1', 'H0STPGM0', '005930'], ['1', 'H0STMKO0', '005930']]

        ### 2-1. 해외주식(미국) 호가, 체결가, 체결통보 ### # 모의투자 해외주식 체결통보: H0GSCNI9
        # code_list = [['1','HDFSASP0','DNASAAPL'],['1','HDFSCNT0','DNASAAPL'],['1','H0GSCNI0','HTS ID를 입력하세요']]

        ### 2-2. 해외주식(미국-주간) 호가, 체결가, 체결통보 ### # 모의투자 해외주식 체결통보: H0GSCNI9
        # code_list = [['1','HDFSASP0','RBAQAAPL'],['1','HDFSCNT0','RBAQAAPL'],['1','H0GSCNI0','HTS ID를 입력하세요']]

        senddata_list=[]

        print("url : ", url)

        for i,j,k in code_list:
            temp = '{"header":{"approval_key": "%s","custtype":"P","tr_type":"%s","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}'%(g_approval_key,i,j,k)
            senddata_list.append(temp)

        async with websockets.connect(url, ping_interval=None) as websocket:

            for senddata in senddata_list:
                await websocket.send(senddata)
                await asyncio.sleep(0.5)
                print(f"Input Command is :{senddata}")

            while True:
                data = await websocket.recv()
                # await asyncio.sleep(0.5)
                print(f"Recev Command is :{data}")  # 정제되지 않은 Request / Response 출력

                if data[0] == '0':
                    recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                    trid0 = recvstr[1]

                    if trid0 == "H0STASP0":  # 주식호가tr 일경우의 처리 단계
                        print("#### 국내주식 호가 ####")
                        stockhoka_domestic(recvstr[3])
                        # await asyncio.sleep(0.2)

                    elif trid0 == "H0STCNT0":  # 주식체결 데이터 처리
                        print("#### 국내주식 체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockspurchase_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2)

                    elif trid0 == "H0STANC0":  # 국내주식 예상체결 데이터 처리
                        print("#### 국내주식 예상체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockexppurchase_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2)  

                    elif trid0 == "H0STOUP0":  # 국내주식 시간외체결 데이터 처리
                        print("#### 국내주식 시간외체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockoverpurchase_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2) 

                    elif trid0 == "H0STOAA0":  # 국내주식 시간외호가 데이터 처리
                        print("#### 국내주식 시간외호가 ####")
                        stockoverhoka_domestic(recvstr[3])
                        # await asyncio.sleep(0.2)                        

                    elif trid0 == "H0STOAC0":  # 국내주식 시간외예상체결데이터 처리
                        print("#### 국내주식 시간외예상체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockoverexppurchase_domestic(data_cnt, recvstr[3])

                    elif trid0 == "H0STMBC0":  # 국내주식 실시간회원사 데이터 처리
                        print("#### 국내주식 실시간회원사 ####")
                        data_cnt = int(recvstr[2])  # 데이터 개수
                        stocksmember_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2) 

                    elif trid0 == "H0STPGM0":  # 국내주식 실시간프로그램매매 데이터 처리
                        print("#### 국내주식 실시간프로그램매매 ####")
                        data_cnt = int(recvstr[2])  # 데이터 개수
                        stocksprogramtrade_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2)                        

                    elif trid0 == "H0STMKO0":  # 국내주식 장운영정보 데이터 처리
                        print("#### 국내주식 장운영정보 ####")
                        data_cnt = int(recvstr[2])  # 데이터 개수
                        stocksmarketinfo_domestic(data_cnt, recvstr[3])  

                    elif trid0 == "H0STNAV0":  # 국내주식 장운영정보 데이터 처리
                        print("#### 국내ETF NAV추이 ####")
                        data_cnt = int(recvstr[2])  # 데이터 개수
                        etfnavtrend_domestic(data_cnt, recvstr[3])

                    elif trid0 == "H0UPCNT0":  # 국내지수 체결 데이터 처리
                        print("#### 국내지수 체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        indexpurchase_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2) 

                    elif trid0 == "H0UPANC0":  # 국내지수 예상체결 데이터 처리
                        print("#### 국내지수 예상체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        indexexppurchase_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2) 

                    elif trid0 == "H0UPPGM0":  # 국내지수 실시간프로그램매매 데이터 처리
                        print("#### 국내지수 실시간프로그램매매 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        indexprogramtrade_domestic(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2)    


                    elif trid0 == "HDFSASP0":  # 해외주식호가tr 일경우의 처리 단계
                        print("#### 해외(미국)주식호가 ####")
                        stockhoka_overseas_usa(recvstr[3])
                        # await asyncio.sleep(0.2)

                    elif trid0 == "HDFSASP1":  # 해외주식호가tr 일경우의 처리 단계
                        print("#### 해외(아시아)주식호가 ####")
                        stockhoka_overseas_asia(recvstr[3])
                        # await asyncio.sleep(0.2)

                    elif trid0 == "HDFSCNT0":  # 해외주식체결 데이터 처리
                        print("#### 해외주식체결 ####")
                        data_cnt = int(recvstr[2])  # 체결데이터 개수
                        stockspurchase_overseas(data_cnt, recvstr[3])
                        # await asyncio.sleep(0.2)
                
                elif data[0] == '1':

                    recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                    trid0 = recvstr[1]

                    if trid0 == "H0STCNI0" or trid0 == "H0STCNI9":  # 주식체결 통보 처리
                        stocksigningnotice_domestic(recvstr[3], aes_key, aes_iv)
                        # await asyncio.sleep(0.2)

                    elif trid0 == "H0GSCNI0" or trid0 == "H0GSCNI9":  # 해외주식체결 통보 처리
                        stocksigningnotice_overseas(recvstr[3], aes_key, aes_iv)
                        # await asyncio.sleep(0.2)
                else:

                    jsonObject = json.loads(data)
                    trid = jsonObject["header"]["tr_id"]

                    if trid != "PINGPONG":
                        rt_cd = jsonObject["body"]["rt_cd"]

                        if rt_cd == '1':  # 에러일 경우 처리

                            if jsonObject["body"]["msg1"] != 'ALREADY IN SUBSCRIBE':
                                print("### ERROR RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))
                            break

                        elif rt_cd == '0':  # 정상일 경우 처리
                            print("### RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))

                            # 체결통보 처리를 위한 AES256 KEY, IV 처리 단계
                            if trid == "H0STCNI0" or trid == "H0STCNI9": # 국내주식
                                aes_key = jsonObject["body"]["output"]["key"]
                                aes_iv = jsonObject["body"]["output"]["iv"]
                                print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))

                            elif trid == "H0GSCNI0": # 해외주식
                                aes_key = jsonObject["body"]["output"]["key"]
                                aes_iv = jsonObject["body"]["output"]["iv"]
                                print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))


                    elif trid == "PINGPONG":
                        print("### RECV [PINGPONG] [%s]" % (data))
                        await websocket.pong(data)
                        print("### SEND [PINGPONG] [%s]" % (data))

    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception as e:
        print('Exception Raised!')
        print(e)
        print('Connect Again!')
        time.sleep(0.1)

        # 웹소켓 다시 시작
        await connect()     
                    
                    
# # 비동기로 서버에 접속한다.
# asyncio.get_event_loop().run_until_complete(connect())
# asyncio.get_event_loop().close()

# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
async def main():
    try:
        # 웹소켓 시작
        await connect()

    except Exception as e:
        print('Exception Raised!')
        print(e)

        
if __name__ == "__main__":

    # noinspection PyBroadException
    try:
        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        # 웹소켓 시작
        asyncio.run(main())

    except KeyboardInterrupt:
        print("KeyboardInterrupt Exception 발생!")
        print(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        print("Exception 발생!")
        print(traceback.format_exc())
        sys.exit(-200)

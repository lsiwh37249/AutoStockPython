"""
종목조회 기본데이터 만듦
"""
import requests
import json
import time
import math
import numpy as np
from datetime import datetime, timedelta


jongTarget = [
    { 'num':	1	,'iscd':'200350', 'name':'래몽래인' },
    { 'num':	2	,'iscd':'950130', 'name':'엑세스바이오'},
    { 'num':	3	,'iscd':'198440', 'name':'고려시멘트'},
    { 'num':	4	,'iscd':'219420', 'name':'링크제니시스'},
    { 'num':	5	,'iscd':'215480', 'name':'토박스코리아'},
    { 'num':	6	,'iscd':'037070', 'name':'파세코'},
    { 'num':	7	,'iscd':'139670', 'name':'키네마스터'},
    { 'num':	8	,'iscd':'030960', 'name':'양지사'},
    { 'num':	9	,'iscd':'189300', 'name':'인텔리안테크'},
    { 'num':	10	,'iscd':'026150', 'name':'특수건설'},
    { 'num':	11	,'iscd':'014970', 'name':'삼륭물산'},
    { 'num':	12	,'iscd':'014910', 'name':'성문전자'},
    { 'num':	13	,'iscd':'234100', 'name':'폴라리스세원'},
    ]

def writeFile(fileName, data):
    f = open(fileName, 'w')
    f.write(json.dumps(data))
    f.close()

jong = []
order = []
url = 'https://openapi.koreainvestment.com:9443'
file = open('acntNo.txt', 'r')
acntNo = file.read().strip()
file.close()

file = open('appKey.txt', 'r')
appKey = file.read().strip()
file.close()

file = open('appSecret.txt', 'r')
appSecret = file.read().strip()
file.close()

hashKey = ''
headers = { "content-type":"application/json",
'appKey': appKey,
'appSecret': appSecret}

dtNow = datetime.now()
dtNowStr = str(dtNow.date()).replace('-','')
dtEnd = str(dtNow.date()).replace('-','')
dtStart = dtNow + timedelta(days=-90)
dtStart = str(dtStart.date()).replace('-','')

print(dtStart + '~' + dtEnd)

inputDate = input('다른 날짜를 입력하시겠습니까? C to Continue, Q to quit, date = date   >>> ')

if inputDate == 'C'  or inputDate == 'c' or inputDate == '':
    print("continue")
elif inputDate == 'Q'  or inputDate == 'q':
    quit()
else:
    dtEnd = inputDate
    print(dtStart + '~' + dtEnd)
    inputTemp = ('any key to continue...')

# 함수정의 #######################################################################

# 일자별시세 --------------------------------------
def getDays30(iscd):
    print("일자별시세###################")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'FHKST01010400',
        'tr_cont':'',
        'custtype':'P',
        #'mac_address':macAddress
        }
    params = {
        'FID_COND_MRKT_DIV_CODE':'J',
        'FID_INPUT_ISCD': iscd,
        'FID_ORG_ADJ_PRC':'0',
        'FID_PERIOD_DIV_CODE':'D'
    }
    sendUrl = url +'/uapi/domestic-stock/v1/quotations/inquire-daily-price'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    #print(res)
    #print(res.headers)
    #print(res.json())
    output = res.json()['output']
    return output

# 기간별시세 --------------------------------------
def getPeriod(iscd, start, end):
    print("기간별시세###################")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'FHKST03010100',
        'tr_cont':'',
        'custtype':'P',
        #'mac_address':macAddress

        }
    params = {
        'FID_COND_MRKT_DIV_CODE':'J',
        'FID_INPUT_ISCD': iscd,
        'FID_INPUT_DATE_1':start,
        'FID_INPUT_DATE_2':end,
        'FID_PERIOD_DIV_CODE':'D',
        'FID_ORG_ADJ_PRC':'0'
    }
    sendUrl = url +'/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    #print(res)
    #print(res.headers)
    #print(res.json())
    output = res.json()['output2']

    return output

# HashKey
def getHashKey(datas):
    sendUrl = url + '/uapi/hashkey'
    res = requests.post(sendUrl, headers=headers, data=json.dumps(datas))
    hashKey = res.json()['HASH']
    return hashKey

# 계좌조회 ----------------------------------
def getAcntList(CTX_AREA_FK100, CTX_AREA_NK100):
    print("잔고조회##############")
    headersDaily = { 
        "content-type":"application/json",
        'appKey': appKey,
        'appSecret': appSecret,
        'authorization': 'Bearer ' + accessToken,
        'tr_id':'TTTC8434R',
        'tr_cont':'',
        'custtype':'P',
        'hashkey': hashKey

        }
    params = {
        'CANO':acntNo,
        'ACNT_PRDT_CD':'01',
        'AFHR_FLPR_YN':'N',
        'OFL_YN':'',
        'INQR_DVSN':'02',
        'UNPR_DVSN':'01',
        'FUND_STTL_ICLD_YN':'N',
        'FNCG_AMT_AUTO_RDPT_YN':'N',
        'PRCS_DVSN':'00',
        'CTX_AREA_FK100':CTX_AREA_FK100,
        'CTX_AREA_NK100':CTX_AREA_NK100
    }
    sendUrl = url +'/uapi/domestic-stock/v1/trading/inquire-balance'
    res = requests.get(sendUrl, headers=headersDaily, params=params)
    return res

# 스토케스틱
def getStochestic(val, hVal, lVal):

    chart_history = []
    chart_h_history = []
    chart_l_history = []
    chart_max_history = []
    chart_min_history = []

    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]:
        chart_history.append(val[index:index + 5])
        chart_h_history.append(hVal[index:index + 5])
        chart_l_history.append(lVal[index:index + 5])
        chart_max_history.append(np.max(chart_h_history[index]))
        chart_min_history.append(np.min(chart_l_history[index]))


    # 스토캐스틱 %K (fast %K) = (현재가격-N일중 최저가)/(N일중 최고가-N일중 최저가) ×100
    st_kf_history = []
    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                    26, 27, 28, 29, 30, 31, 32, 33, 34]:
        st_kf_history.append(
            (chart_history[index][0] - chart_min_history[index]) / (
                    chart_max_history[index] - chart_min_history[index]) * 100)

    st_k_history = []
    st_d_history = []
    for index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                    26, 27, 28, 29, 30, 31, 32, 33, 34]:
        st_k_history.append(np.average(st_kf_history[index:index + 3]))
    
    return st_k_history[0]

#######################################################################


# 인증키
def getToken(appKey, appSecret):
    body = {"grant_type":"client_credentials",
            "appkey":appKey, 
            "appsecret":appSecret}

    sendUrl = url + '/oauth2/tokenP'
    res = requests.post(sendUrl, headers=headers, data=json.dumps(body))
    print(res)
    accessToken = res.json()['access_token']
    print(accessToken)
    return accessToken

accessToken = getToken(appKey, appSecret)

# 계좌잔고 가져오기
def getAccountInfo():
    acntData = getAcntList('','')
    acntJson = acntData.json()
    acntHeader = acntData.headers

    if acntJson['rt_cd'] != '0':
        print("계좌가져오기 오류")
        print(acntJson)
        quit()

    acntJsonOutput1 = acntJson['output1']
    jongTemp = []
    for item in acntJsonOutput1:
        jongTemp.append({
                'iscd': item['pdno'],
                'name': item['prdt_name'],
                'price': int(item['prpr']),
                'amto' : int(item['pchs_amt']),
                'amt': int(item['evlu_amt']),
                'profit': int(item['evlu_pfls_amt']),
                'qty':int(item['hldg_qty'])
            })

    print("보유 제외종목##########################")
    return jongTemp

jongTemp = getAccountInfo()

jongAll = []

for item in jongTarget:
    existJongTemp = False
    for item2 in jongTemp:
        if item['iscd'] == item2['iscd']:
            item['price'] = item2['price']
            item['amto'] = item2['amto']
            item['amt'] = item2['amt']
            item['profit'] = item2['profit']
            item['qty'] = item2['qty']
            existJongTemp = True
    jongAll.append(item)

for item in jongAll:
    if item.get('qty'):
        item['exist'] = True
    else: 
        item['qty'] = 0
        item['exist'] = False


# 종목별 일자별 시세
for index, item in enumerate(jongAll):
    chartValue = []
    chartHigh = []
    chartLow = []
    chartDate = []
    time.sleep(0.3)
    
    chartData = getPeriod(item['iscd'], dtStart, dtEnd)
    for item2 in chartData:
        chartDate.append(item2['stck_bsop_date'])
        chartValue.append(int(item2['stck_clpr']))
        chartHigh.append(int(item2['stck_hgpr']))
        chartLow.append(int(item2['stck_lwpr']))
    
    item['rate'] = int((int(chartValue[0])-int(chartValue[1]))/int(chartValue[1]) * 1000)/1000
    item['price'] = int(chartValue[0])

    bfChartValue = chartValue[1::]
    bfChartHigh = chartHigh[1::]
    bfChartLow = chartLow[1::]

    item['st'] = int(getStochestic(chartValue, chartHigh, chartLow) * 1000)/1000
    item['stBf'] = int(getStochestic(bfChartValue, bfChartHigh, bfChartLow) * 1000)/1000
    item['updateDate'] = dtEnd


print("일자별데이터, 계좌잔액 정리########################")
writeFile('baseData' + dtNowStr + '.json', jongAll)
#print(jongAll)
print("name | st | rate | updateDate")
for index, item in enumerate(jongAll):
    print(item['name'] + ' ' + str(item['st']) + ' ' + str(item['rate']) + ' ' + item['updateDate'])

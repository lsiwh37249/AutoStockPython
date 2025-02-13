from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from KISRealtime import connect

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 연결된 WebSocket 클라이언트를 저장할 set

@app.websocket("/ws_test")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        g_appkey = os.getenv("APPKEY")
        g_appsecret = os.getenv("SECRETKEY")
        g_approval_key= get_approval(g_appkey, g_appsecret)
        print("approval_key [%s]" % (g_approval_key))

        # url = 'ws://ops.koreainvestment.com:31000' # 모의투자계좌
        url = 'ws://ops.koreainvestment.com:21000' # 실전투자계좌

        # 원하는 호출을 [tr_type, tr_id, tr_key] 순서대로 리스트 만들기

        ### 1-1. 국내주식 호가, 체결가, 예상체결, 체결통보 ### # 모의투자 국내주식 체결통보: H0STCNI9
        code_list = [['1','H0STASP0','005930'],['1','H0STCNT0','005930'],['1', 'H0STANC0', '005930'],['1','H0STCNI0','1069149']]

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

            
            data = await websocket.recv()
            # await asyncio.sleep(0.5)
            print(f"Recev Command is :{data}")  # 정제되지 않은 Request / Response 출력

            if data[0] == '0':
                recvstr = data.split('|')  # 수신데이터가 실데이터 이전은 '|'로 나뉘어져있어 split
                trid0 = recvstr[1]
                if trid0 == "H0STASP0":  # 주식호가tr 일경우의 처리 단계
                    print("#### 국내주식 호가 ####")
                    #stockhoka_domestic(recvstr[3])
                    return recvstr[3]
                    # await asyncio.sleep(0.2)
    except:
        pass

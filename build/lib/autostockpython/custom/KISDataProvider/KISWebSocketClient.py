import websockets
import os
import time
import requests
import json
from fastapi import FastAPI, WebSocket

# WebSocket 클라이언트 관리 클래스
class KISWebSocketClient:
    def __init__(self):
        self.clients = set()  # 연결된 클라이언트 저장
        self.url = "wss://ops.koreainvestment.com:21000"  # 실전투자 WebSocket URL
        self.g_appkey = os.getenv("APPKEY")
        self.g_appsecret = os.getenv("SECRETKEY")
        self.g_approval_key = None
        self.websocket = None  # 한국투자증권 WebSocket

    @staticmethod
    def get_approval(key, secret):                                            # url = https://openapivts.koreainvestment.com:29443' # 모의투자계좌
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
        print(approval_key)
        return approval_key

    async def connect_kis_api(self):
        """ 한국투자증권 WebSocket API와 연결 """
        try:
            # API 승인키 요청
            self.g_approval_key = self.get_approval(self.g_appkey, self.g_appsecret)
            print(f"✅ 승인키: {self.g_approval_key}")

            # 실시간 종목 요청 리스트
            code_list = [
                ['1', 'H0STASP0', '005930'],  # 호가
                ['1', 'H0STCNT0', '005930'],  # 체결가
                ['1', 'H0STANC0', '005930'],  # 예상체결
                ['1', 'H0STCNI0', '1069149']  # 체결통보
            ]

            senddata_list = []
            for i, j, k in code_list:
                temp = json.dumps({
                    "header": {
                        "approval_key": self.g_approval_key,
                        "custtype": "P",
                        "tr_type": i,
                        "content-type": "utf-8"
                    },
                    "body": {
                        "input": {
                            "tr_id": j,
                            "tr_key": k
                        }
                    }
                })
                senddata_list.append(temp)

            # WebSocket 연결
            async with websockets.connect(self.url, ping_interval=None) as kis_ws:
                self.websocket = kis_ws  # 연결된 WebSocket 저장

                # 종목 요청 전송
                for senddata in senddata_list:
                    await kis_ws.send(senddata)
                    await asyncio.sleep(0.5)  # 요청 간격 조절
                    print(f"📩 요청 전송: {senddata}")

                # 실시간 데이터 수신
                while True:
                    data = await kis_ws.recv()
                    print(f"📊 받은 데이터: {data}")
                    # 연결된 모든 클라이언트에게 데이터 전송
                    await self.broadcast(data)

        except Exception as e:
            print(f"❌ 오류 발생: {e}")

    async def broadcast(self, message: str):
        """ 모든 연결된 클라이언트에게 메시지 전송 """
        for client in self.clients:
            await client.send_text(message)

    async def register_client(self, websocket: WebSocket):
        """ WebSocket 클라이언트 등록 및 메시지 처리 """
        await websocket.accept()
        self.clients.add(websocket)
        try:
            while True:
                message = await websocket.receive_text()
                print(f"📨 클라이언트 메시지: {message}")
                await websocket.send_text(f"서버 응답: {message}")

        except WebSocketDisconnect:
            print("❌ 클라이언트 연결 종료")
        finally:
            self.clients.remove(websocket)


from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import os
from autostockpython.custom.KISDataProvider.KISWebSocketClient import KISWebSocketClient
import websockets


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

kis_client = KISWebSocketClient()  # 한국투자증권 WebSocket 클라이언트 객체 생성


@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    """ 클라이언트 WebSocket 연결 핸들러 """
    await kis_client.register_client(websocket)

@app.on_event("startup")
async def startup_event():
    """ FastAPI 서버 시작 시 한국투자증권 WebSocket 연결 """
    asyncio.create_task(kis_client.connect_kis_api())


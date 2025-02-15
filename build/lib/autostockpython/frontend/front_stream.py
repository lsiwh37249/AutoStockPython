import streamlit as st
import websocket
import threading
import json

# WebSocket 클라이언트 설정
def on_message(ws, message):
    data = json.loads(message)
    st.session_state["latest_data"] = data

def on_error(ws, error):
    st.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    st.warning("WebSocket connection closed")

def websocket_thread():
    ws = websocket.WebSocketApp("ws://localhost:8000/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

# Streamlit 앱 시작
st.title("실시간 호가 데이터")

#초기화
if "latest_data" not in st.session_state:
    st.session_state["latest_data"] = {}

if st.button("연결 시작"):
    threading.Thread(target=websocket_thread, daemon=True).start()

# 실시간 데이터 표시
if st.session_state["latest_data"]:
    data = st.session_state["latest_data"]
    st.write(f"현재가: {data['price']}")
    st.write(f"거래량: {data['volume']}")
else:
    st.write("데이터를 기다리는 중...")

from fastapi import FastAPI, WebSocket

app = FastAPI()

async def print(websocket):
    

@app.websocket("/ws")
async def webscoket_handler(websocket: WebSocket):
    await 

import asyncio
import websockets

async def handle_connection(websocket, path):
    # 當有新的 WebSocket 連接建立時，這個函數將被呼叫

    while True:
        try:
            data = await websocket.recv()  # 接收來自客戶端的數據
            # 在這裡處理收到的數據
            print(f"Received data: {data}")

            # 對數據進行處理後，你可以選擇向客戶端發送回覆
            response = f"Processed: {data}"
            await websocket.send(response)
        except websockets.exceptions.ConnectionClosedError:
            break

start_server = websockets.serve(handle_connection, "140.131.114.149", 80)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever() 

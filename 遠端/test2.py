import asyncio
import websockets

async def send_data():
    uri = "ws://140.131.114.149:80"  # 請替換為虛擬機的 IP 地址和端口

    async with websockets.connect(uri) as websocket:
        while True:
            data = input("輸入要發送的數據: ")
            await websocket.send(data)  # 向服務端發送數據

            response = await websocket.recv()  # 接收服務端的回覆
            print(f"Received response: {response}")

asyncio.get_event_loop().run_until_complete(send_data())
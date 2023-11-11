import sys
import argparse
import asyncio
import websockets

async def send_data(xpath):
    uri = "ws://140.131.114.149:80"  # 請替換為虛擬機的 IP 地址和端口

    async with websockets.connect(uri) as websocket:
        message = f"xpath, {xpath}"
        await websocket.send(message)
        response = await websocket.recv()
        return response

async def main_async(xpath):
    response = await send_data(xpath)
    print(f"{response}")
    # 在這裡進行其他的操作

async def websocket_handler(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        # 处理消息并发送响应


def main():
    # 處理命令列參數
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("xpath", type=str, help="Account for authentication")
    
    args = parser.parse_args()

    # 在這裡使用 args.account 和 args.password 進行相應的操作
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async(args.xpath))

if __name__ == '__main__':
    main()

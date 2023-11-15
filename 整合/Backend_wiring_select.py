import sys
import argparse
import asyncio
import websockets

async def send_data(username):
    uri = "ws://140.131.114.149:80"

    async with websockets.connect(uri) as websocket:
        message = f"select, {username}"
        await websocket.send(message)
        response = await websocket.recv()
        return response

async def main_async(username):
    response = await send_data(username)
    print(f"{response}")
    # 在這裡進行其他的操作

async def main():
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("username", type=str, help="username for authentication")

    args = parser.parse_args()
    
    # 使用 gather 等待 main_async 完成
    await asyncio.gather(main_async(args.username))

if __name__ == '__main__':
    # 使用 asyncio.run 來運行 main 函數
    asyncio.run(main())

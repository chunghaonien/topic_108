import sys
import argparse
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError

async def send_data(user_id):
    uri = "ws://140.131.114.149:80"

    try:
        async with websockets.connect(uri) as websocket:
            message = f"select, {user_id}"
            await websocket.send(message)
            response = await websocket.recv()
            return response
    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main_async(user_id):
    response = await send_data(user_id)
    print(f"{response}")
    # 在這裡進行其他的操作

async def main():
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("user_id", type=str, help="user_id for authentication")

    args = parser.parse_args()
    
    # 使用 gather 等待 main_async 完成
    await asyncio.gather(main_async(args.user_id))

if __name__ == '__main__':
    # 使用 asyncio.run 來運行 main 函數
    asyncio.run(main())


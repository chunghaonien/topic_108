import sys
import argparse
import asyncio
import websockets

async def send_data(account, password, username):
    uri = "ws://140.131.114.149:80"  # 請替換為虛擬機的 IP 地址和端口

    async with websockets.connect(uri) as websocket:
        message = f"register, {account}, {password}, {username}"
        await websocket.send(message)
        response = await websocket.recv()
        return response

async def main_async(account, password, username):
    response = await send_data(account, password, username)
    print(f"{response}")
    # 在這裡進行其他的操作

def main():
    # 處理命令列參數
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("account", type=str, help="Account for authentication")
    parser.add_argument("password", type=str, help="Password for authentication")
    parser.add_argument("username", type=str, help="Username for authentication")

    args = parser.parse_args()

    # 在這裡使用 args.account 和 args.password 進行相應的操作
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async(args.account, args.password, args.username))

if __name__ == '__main__':
    main()

import sys
import argparse
import asyncio
import websockets

async def send_data(account, password):
    uri = "ws://140.131.114.149:80"  # 請替換為虛擬機的 IP 地址和端口

    async with websockets.connect(uri) as websocket:
        message = f"login, {account}, {password}"

        # 向服務端發送包含帳號和密碼的訊息
        await websocket.send(message)

        response = await websocket.recv()  # 接收服務端的回覆
        print(f"Received response: {response}")

def main():
    # 處理命令列參數
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("account", type=str, help="Account for authentication")
    parser.add_argument("password", type=str, help="Password for authentication")

    args = parser.parse_args()
# 在這裡使用 args.account 和 args.password 進行相應的操作
    asyncio.get_event_loop().run_until_complete(send_data(args.account, args.password))

if __name__ == '__main__':
    main()

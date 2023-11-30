import sys
import argparse
import asyncio
import websockets

async def upload_data(user_id, scraped_data):
    uri = "ws://140.131.114.149:80"  # 請替換為虛擬機的 IP 地址和端口

    async with websockets.connect(uri) as websocket:
        message = f"upload, {user_id}, {scraped_data}"
        await websocket.send(message)
        response = await websocket.recv()
        return response

async def main_async(user_id, scraped_data):
    response = await upload_data(user_id, scraped_data)
    print(f"{response}")
    # 在這裡進行其他的操作

async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # 在這裡進行消息處理，並根據需要發送回應
            response_message = f"Received and processed: {message}"
            await websocket.send(response_message)
    except websockets.WebSocketException as e:
        print(f"WebSocket error: {e}")
        # 處理錯誤，可能需要重新連接或採取其他操作

async def main(): 
    # 處理命令列參數
    parser = argparse.ArgumentParser(description="Backend wiring with WebSocket")
    parser.add_argument("user_id", type=str, help="User_ID for Database")
    parser.add_argument("scraped_data", type=str, help="Scraped_Data for Database")
    
    args = parser.parse_args()

    # 在這裡使用 args.user_id 和 args.scraped_data 進行相應的操作
    await asyncio.gather(main_async(args.user_id, args.scraped_data))

if __name__ == '__main__':
    asyncio.run(main())
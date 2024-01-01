import sys
import argparse
import asyncio
import websockets
import json  # 添加导入语句
from websockets.exceptions import ConnectionClosedError

# 在 Backend_wiring_select.py 中
async def send_data(user_id):
    uri = "ws://140.131.114.149:80"

    try:
        async with websockets.connect(uri) as websocket:
            message = f"select, {user_id}"  # 使用字典代替字符串
            await websocket.send(message)
            response = await websocket.recv()
            # 在 Backend_wiring_select.py 的 main_async 函数内添加以下打印语句

            return response  # 將 response 返回
    except ConnectionClosedError as e:
        print(f"WebSocket connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main_async(user_id):
    response = await send_data(user_id)
    return response  # 返回 response
    

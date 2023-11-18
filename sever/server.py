import asyncio
import websockets
from MemberSystem import login_system, register_system
from Comparison import data_Comparison
from Select_Data import selectdata
from ScrapSystem import upload_result



async def handle_connection(websocket, path):
    # 當有新的 WebSocket 連接建立時，這個函數將被呼叫
    
    while True:
        try:
            data = await websocket.recv()  # 接收來自客戶端的數據
            # 在這裡處理收到的數據
            data_list = data.split(", ")

            # 初始化 response 變數
            response = "Invalid request"  # 或者使用其他適當的預設值
            user_id = ""
            print(data_list)
            
            # 判斷類別
            if data_list[0] == 'login':
                response = str(login_system.login(data_list[1], data_list[2]))
                print(response)
                # user_id = login_system.login_id(data_list[1], data_list[2])
            elif data_list[0] == 'register':
                response = str(register_system.register(data_list[1], data_list[2], data_list[3]))
            elif data_list[0] == 'xpath':
                data_list.pop(0)

                dou_data = []
                dou_data.append(data_list)

                # 呼叫 data_Comparison.data_process 並將結果傳給 response
                cleaned_data = [item.replace('"[', "").replace('"]', "").strip() for item in dou_data[0]]

                result = data_Comparison.data_process(cleaned_data)
                # print(result)
                response = str(result)
            elif data_list[0] == 'select':
                response = selectdata
            elif data_list[0] == 'upload':
                response = str(upload_result.upload_scrape_data(int(data_list[1]), data_list[2]))

            # if user_id != "":
            #     await websocket.send(response, user_id)
            # else:
            await websocket.send(response)

        except websockets.exceptions.ConnectionClosedError:
           
            break
        except websockets.exceptions.ConnectionClosedOK:
            break
            

        # 休眠一小段時間，以減少 CPU 使用率
        await asyncio.sleep(0.1)

start_server = websockets.serve(handle_connection, "140.131.114.149", 80)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

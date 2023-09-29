import pyautogui
import time

def record_script():
    print("Recording script...")
    script = []

    try:
        while True:
            time.sleep(1)  # 等待1秒，给你时间切换到浏览器窗口
            x, y = pyautogui.position()
            action_type = "move"
            
            # 如果鼠标左键被按下，记录点击事件
            if pyautogui.mouseDown():
                action_type = "click"

            action = {"action": action_type, "x": x, "y": y}
            script.append(action)

    except KeyboardInterrupt:
        print("Recording stopped.")
        return script

if __name__ == "__main__":
    recorded_script = record_script()
    print("Recorded Script:", recorded_script)

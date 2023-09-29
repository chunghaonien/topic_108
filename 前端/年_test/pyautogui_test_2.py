import time
import pyautogui

def record_script():
    print("Recording script...")
    script = []

    try:
        while True:
            time.sleep(1)  # 休眠1秒钟以便你有时间切换到浏览器窗口
            x, y = pyautogui.position()
            action = {"action": "move", "x": x, "y": y}
            script.append(action)

    except KeyboardInterrupt:
        print("Recording stopped.")
        return script

def play_script(script):
    print("Playing script...")
    for action in script:
        x, y = action["x"], action["y"]
        pyautogui.moveTo(x, y)

if __name__ == "__main__":
    # 记录脚本
    recorded_script = record_script()

    # 播放脚本
    play_script(recorded_script)

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from nova_orbit import NovaChatWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Nova-Orbit Framework")
    window.resize(900, 700)
    window.setStyleSheet("background-color: #121212;")

    # ⚠️ 请替换为你的真实 Key
    chat = NovaChatWidget(api_key="sk-你的DeepSeek_API_KEY")

    # 演示系统日志注入接口（如果用户自己开发了 Agent，可以调用这个接口）
    # chat.add_log("正在扫描本地文件...")

    window.setCentralWidget(chat)
    window.show()
    sys.exit(app.exec())

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl
from .bridge import NovaChatBridge


class NovaChatWidget(QWidget):
    """开箱即用的 QWidget 封装，支持直接嵌入任何 PySide 应用"""

    def __init__(self, api_key: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #121212;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.quick_widget = QQuickWidget()
        self.quick_widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)

        self.bridge = NovaChatBridge(api_key=api_key)

        # 将 Python 桥接对象注入到 QML 环境
        engine = self.quick_widget.engine()
        engine.rootContext().setContextProperty("bridge", self.bridge)

        # 加载打包在库里的 QML 文件
        qml_path = os.path.join(os.path.dirname(__file__), "qml", "NovaChatWindow.qml")
        self.quick_widget.setSource(QUrl.fromLocalFile(qml_path))

        layout.addWidget(self.quick_widget)

        # 暴露日志接口给外部
        self.add_log = self.bridge.add_system_log
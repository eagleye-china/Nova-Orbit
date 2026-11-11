import threading
from PySide6.QtCore import QObject, Slot, Property, QAbstractListModel, QModelIndex, Qt, QTimer
from openai import OpenAI


class MessageModel(QAbstractListModel):
    TextRole = Qt.ItemDataRole.UserRole + 1
    IsUserRole = Qt.ItemDataRole.UserRole + 2
    IsSystemRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self):
        super().__init__()
        self._messages = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._messages)

    def data(self, index, role):
        if not index.isValid(): return None
        msg = self._messages[index.row()]
        if role == self.TextRole: return msg.get("text", "")
        if role == self.IsUserRole: return msg.get("isUser", False)
        if role == self.IsSystemRole: return msg.get("isSystem", False)
        return None

    def roleNames(self):
        return {
            self.TextRole: b"text",
            self.IsUserRole: b"isUser",
            self.IsSystemRole: b"isSystem"
        }

    def add(self, text, is_user=False, is_sys=False):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._messages.append({"text": text, "isUser": is_user, "isSystem": is_sys})
        self.endInsertRows()

    def update_last(self, text):
        if self._messages:
            self._messages[-1]["text"] = text
            idx = self.index(len(self._messages) - 1, 0)
            self.dataChanged.emit(idx, idx, [self.TextRole])


class NovaChatBridge(QObject):
    """核心桥接器：处理 API 请求、数据模型与 QML 的交互"""

    def __init__(self, api_key: str, base_url="https://api.deepseek.com", model="deepseek-chat"):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

        self._model = MessageModel()
        self._model.add("Hello! I am Nova-Orbit. How can I assist you today?", False)

        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self._current_ai_text = ""
        self._is_streaming = False

        self._timer = QTimer()
        self._timer.setInterval(50)
        self._timer.timeout.connect(self._update_ui_stream)

    @Property(QObject, constant=True)
    def messagesModel(self):
        return self._model

    @Slot(str)
    def send_user_message(self, text):
        if not text.strip() or self._is_streaming: return

        self._model.add(text, True)
        self.messages.append({"role": "user", "content": text})

        self._current_ai_text = ""
        self._model.add("Thinking...", False)
        self._is_streaming = True
        self._timer.start()

        threading.Thread(target=self._fetch_ai_response, daemon=True).start()

    @Slot(str)
    def add_system_log(self, text):
        """对外暴露的接口，可用于记录 Agent 的思考过程或工具调用"""
        self._model.add(f"⚙️ {text}", False, is_sys=True)

    def _fetch_ai_response(self):
        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=self.messages,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    self._current_ai_text += chunk.choices[0].delta.content
            self.messages.append({"role": "assistant", "content": self._current_ai_text})
        except Exception as e:
            self._current_ai_text = f"⚠️ API Error: {str(e)}"
        finally:
            self._is_streaming = False

    def _update_ui_stream(self):
        if self._current_ai_text:
            self._model.update_last(self._current_ai_text)
        if not self._is_streaming and self._current_ai_text:
            self._timer.stop()
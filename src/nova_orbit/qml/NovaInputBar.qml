import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    signal sendMessage(string text)
    height: Math.min(150, Math.max(60, inputScroll.contentHeight + 20))

    Rectangle {
        anchors.fill: parent
        radius: 8
        color: "#263238"
        border.color: inputArea.activeFocus ? "#0277BD" : "#37474F"
        border.width: 1
        Behavior on border.color { ColorAnimation { duration: 200 } }

        ScrollView {
            id: inputScroll
            anchors.left: parent.left
            anchors.right: sendBtn.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 12
            anchors.rightMargin: 10
            clip: true

            TextArea {
                id: inputArea
                placeholderText: "Type a message... (Enter to send, Shift+Enter for new line)"
                color: "#ECEFF1"
                font.pixelSize: 14
                wrapMode: TextArea.Wrap
                background: Item {}
                selectByMouse: true

                Keys.onPressed: (event) => {
                    if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                        if (event.modifiers & Qt.ShiftModifier) {
                            event.accepted = false;
                        } else {
                            if (inputArea.text.trim() !== "") {
                                root.sendMessage(inputArea.text.trim());
                                inputArea.text = "";
                            }
                            event.accepted = true;
                        }
                    }
                }
            }
        }

        Button {
            id: sendBtn
            text: "🚀"
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 10
            width: 40
            height: 40
            background: Rectangle { color: "#0277BD"; radius: 6 }
            contentItem: Text { text: "🚀"; anchors.centerIn: parent; font.pixelSize: 18 }

            visible: opacity > 0
            opacity: inputArea.text.trim() !== "" ? 1.0 : 0.0
            scale: inputArea.text.trim() !== "" ? 1.0 : 0.5
            Behavior on opacity { NumberAnimation { duration: 150 } }
            Behavior on scale { NumberAnimation { duration: 150; easing.type: Easing.OutBack } }

            onClicked: {
                if (inputArea.text.trim() !== "") {
                    root.sendMessage(inputArea.text.trim());
                    inputArea.text = "";
                }
            }
        }
    }
}
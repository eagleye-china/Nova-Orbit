import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    width: 800; height: 600
    property color bgColor: "#121212"

    Rectangle {
        anchors.fill: parent
        color: bgColor

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 15
            spacing: 10

            ListView {
                id: listView
                Layout.fillWidth: true
                Layout.fillHeight: true
                model: bridge.messagesModel
                spacing: 15
                clip: true

                delegate: NovaMessageBubble {
                    width: listView.width
                    text: model.text
                    isUser: model.isUser
                    isSystem: model.isSystem
                }
                onCountChanged: listView.positionViewAtEnd()
            }

            NovaInputBar {
                id: inputBar
                Layout.fillWidth: true
                onSendMessage: (text) => {
                    bridge.send_user_message(text)
                }
            }
        }
    }
}
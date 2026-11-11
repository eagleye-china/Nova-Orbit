import QtQuick
import QtQuick.Controls

Item {
    id: root
    property string text: ""
    property bool isUser: false
    property bool isSystem: false
    height: bubbleRect.height + 10

    Rectangle {
        id: bubbleRect
        anchors.right: isUser ? parent.right : undefined
        anchors.left: isUser ? undefined : parent.left
        width: Math.min(bubbleText.implicitWidth + 30, root.width * 0.75)
        height: bubbleText.implicitHeight + 24
        radius: isSystem ? 4 : 10
        color: isUser ? "#0277BD" : (isSystem ? "#1E272E" : "#263238")
        border.color: isSystem ? "#2E7D32" : "transparent"
        border.width: isSystem ? 1 : 0

        Text {
            id: bubbleText
            text: root.text || ""
            anchors.centerIn: parent
            width: parent.width - 30
            wrapMode: Text.Wrap
            color: isSystem ? "#4CAF50" : "#ECEFF1"
            font.pixelSize: isSystem ? 12 : 14
            font.family: isSystem ? "Consolas" : "Microsoft YaHei"
            textFormat: Text.PlainText
        }
    }
}
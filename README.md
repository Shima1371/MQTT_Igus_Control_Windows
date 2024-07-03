# Control igus Through MQTT (2024/07/03)

MQTT でのメッセージを受け取って、
igus を Ethernet 経由で制御かつ
SRTのSCB-PB（ソフトグリッパーの空圧制御）をModbus RTU通信で制御

Windowsで動作確認済、linuxはmodbus通信周りがうまくいくかわかりません。少なくともself.modbus_clientのポート名を変更する必要あり（他にもなんかあるかも）

CRI Ethernet Interface
https://wiki.cpr-robots.com/index.php/CRI_Ethernet_Interface
(CRI V17 (since iRC/CPRog V14))

SCB-PB
https://www.softrobottech.com/web/jp/download?type=1&title=SCB-PB

(SCB-PBのcommunication protocolが公式HPに無い、手元にpdf有)


参考：https://github.com/nkawa/MQTT_Dobot_Nova2_Control

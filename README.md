# Control igus Through MQTT (2024/07/12)

MQTT でのメッセージを受け取って、
igus を Ethernet 経由で制御かつ
SRTのSCB-PB（ソフトグリッパーの空圧制御）をModbus RTU通信で制御

Windowsで動作確認済、linuxはmodbus通信周りがうまくいくかわかりません。少なくともself.modbus_clientのポート名を変更する必要あり（他にもなんかあるかも）

## 準備
### ライブラリのインストール
```
pip install paho-mqtt
pip install pymodbus
pip install pyserial
```
pyserialはコード内で明示的にimportしていないが、なんか無いと動かない。

### IPアドレスの変更
ロボット(192.168.3.11)と同一サブネット上にいる必要がある。以下の設定でうまくいくはず。

* IPアドレス: 192.168.3.xxx（xxxは1と11以外ならおそらく問題ない)
* サブネットマスク: 255.255.255.0
* (デフォルト)ゲートウェイ: 192.168.3.1
* 優先DNS: 192.168.3.1

以下はigus公式の説明

https://blog.igus.eu/how-to-connect-the-igus-robot-control-to-your-pc/


## 参考

CRI Ethernet Interface
https://wiki.cpr-robots.com/index.php/CRI_Ethernet_Interface
(CRI V17 (since iRC/CPRog V14))

SCB-PB
https://www.softrobottech.com/web/jp/download?type=1&title=SCB-PB

(SCB-PBのcommunication protocolが公式HPに無い、手元にpdf有)


参考：https://github.com/nkawa/MQTT_Dobot_Nova2_Control

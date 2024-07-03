from pymodbus.client import ModbusSerialClient as ModbusClient

# Modbus RTUクライアントの設定
client = ModbusClient(method='rtu', port='COM3',stopbits=1, bytesize=8, parity='N', baudrate=38400, timeout=3) #baudrate=38400

# クライアントの接続
connection = client.connect()

# 接続確認
if connection:
    print("クライアントの接続成功")

    # デバイスにコマンドを送信
    # response = client.read_input_registers(address=6, count=1, slave=1)
    response = client.write_register(address=1, value=1, slave=1)
    
    # # レスポンスの確認
    if not response.isError():
        print(response.registers)
    else:
        print("エラー:", response)

    # クライアントの切断
    client.close()
else:
    print("クライアントの接続失敗")
    client.close()


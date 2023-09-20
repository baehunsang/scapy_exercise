import asyncio
import json
import random
import websockets

async def send_fuzzed_boot_notification():
    # WebSocket 연결 설정
    async with websockets.connect("ws://localhost:9000", subprotocols=["ocpp1.6"]) as websocket:
        for _ in range(10):  # 덤브 퍼저를 10번 실행
            # 임의의 데이터를 생성하여 BootNotification 메시지에 주입
            boot_notification_data = {
                "chargingStation": {
                    "vendorName": f"Vendor_{random.randint(1, 100)}",
                    "modelName": f"Model_{random.randint(1, 100)}",
                },
                "chargingStationSerialNumber": str(random.randint(1, 10000)),
                "firmwareVersion": f"FW_{random.uniform(1, 10)}"
            }

            ocpp_message = {
                "chargePointVendor": "Vendor",
                "chargePointModel": "Model",
                "chargePointSerialNumber": "12345",
                "chargeBoxSerialNumber": "54321",
                "firmwareVersion": "1.0",
                "iccid": "1234567890",
                "imsi": "0987654321",
                "meterSerialNumber": "9876543210",
                "meterType": "type123",
                "bootReason": "PowerUp",
                "chargingStation": boot_notification_data
            }

            # 무작위로 변경된 BootNotification 메시지를 서버로 전송
            print("Sending fuzzed message:", ocpp_message)
            await websocket.send(json.dumps(ocpp_message))
            
            # 서버로부터 응답 받기 (필요한 경우)
            response = await websocket.recv()
            print("Received response:", response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_fuzzed_boot_notification())


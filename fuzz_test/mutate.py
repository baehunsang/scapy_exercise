import asyncio
import json
import random
import websockets
import subprocess
import threading


async def send_fuzzed_boot_notification():
    # WebSocket 연결 설정
    async with websockets.connect("ws://localhost:9000", subprotocols=["ocpp1.6"]) as websocket:
        for _ in range(100):  
            
            #Mutation ??
            ocpp_message = [
                                2,
                                "A x 12288",
                                "BootNotification",
                                {
                                    "chargePointModel":"Optimus",
                                    "chargePointVendor":"The Mobility House",
                                    "chargePointSerialNumber": "111111111111"
                                }
                            ]
            # 필드 무작위 변조
            ocpp_message[3]["chargePointModel"] = random.choice(["ModelA", "0xffffffff", "%99999999999s", "%x%x%x%x%c%n%b", "\xcc\xcc\xcc\xcc%x%x%x%n"])
            ocpp_message[3]["chargePointVendor"] = random.choice(["VendorX", "VendorY", "VendorZ"])
            ocpp_message[3]["chargePointSerialNumber"] = random.choice(["\r\n", "%n"])

            # 무작위로 변경된 BootNotification 메시지를 서버로 전송
            print("Sending fuzzed message:", ocpp_message)
            await websocket.send(json.dumps(ocpp_message))
            
            # 서버로부터 응답 받기 (필요한 경우)
            response = await websocket.recv()
            print("Received response:", response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_fuzzed_boot_notification())


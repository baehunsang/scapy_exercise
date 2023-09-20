import asyncio
import json
import random
import websockets

async def send_fuzzed_boot_notification():
    # WebSocket 연결 설정
    async with websockets.connect("ws://localhost:9000", subprotocols=["ocpp1.6"]) as websocket:
        for _ in range(10):  
            
            #Mutation ??
            ocpp_message = [
                                2,
                                "93e69619-58c7-49a8-bbf6-3f418ef172e9",
                                "BootNotification",
                                {"chargePointModel":"Optimus",
                                    "chargePointVendor":"The Mobility House"
                                }
                            ]

            # 무작위로 변경된 BootNotification 메시지를 서버로 전송
            print("Sending fuzzed message:", ocpp_message)
            await websocket.send(json.dumps(ocpp_message))
            
            # 서버로부터 응답 받기 (필요한 경우)
            response = await websocket.recv()
            print("Received response:", response)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(send_fuzzed_boot_notification())
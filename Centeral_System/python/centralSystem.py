import asyncio
import logging
from datetime import datetime

try:
    import websockets
    import pymysql
except ModuleNotFoundError:
    print("This example relies on the 'websockets' and 'pymysql' packages.")
    print("Please install them by running: ")
    print()
    print(" $ pip install websockets pymysql")
    import sys

    sys.exit(1)

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus

logging.basicConfig(level=logging.INFO)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'ocpp',
    'password': 'password123',
    'database': 'OCPP_CentralSystem',
}

class ChargePoint(cp):
    @on(Action.BootNotification)
    async def on_boot_notification(
        self, charge_point_vendor: str, charge_point_model: str, **kwargs
    ):
        # Connect to MySQL Database
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # Query the database to check if the charge point is valid
        cursor.execute(
            "SELECT * FROM boot_notification WHERE chargePointVendor = %s AND chargePointModel = %s",
            (charge_point_vendor, charge_point_model)
        )
        result = cursor.fetchone()
        
        if result:
            # If a matching record is found in the database, accept the boot notification
            status = RegistrationStatus.accepted
            print("accepted charging station")
        else:
            # If no matching record is found, reject the boot notification
            status = RegistrationStatus.rejected
            print("rejected charging station")
        
        # Close the database connection
        cursor.close()
        db_connection.close()

        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=status,
        )

async def on_connect(websocket, path):
    """For every new charge point that connects, create a ChargePoint
    instance and start listening for messages.
    """
    try:
        requested_protocols = websocket.request_headers["Sec-WebSocket-Protocol"]
    except KeyError:
        logging.error("Client hasn't requested any Subprotocol. Closing Connection")
        return await websocket.close()
    if websocket.subprotocol:
        logging.info("Protocols Matched: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning(
            "Protocols Mismatched | Expected Subprotocols: %s,"
            " but client supports  %s | Closing connection",
            websocket.available_subprotocols,
            requested_protocols,
        )
        return await websocket.close()

    charge_point_id = path.strip("/")
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect, "0.0.0.0", 9000, subprotocols=["ocpp1.6"]
    )

    logging.info("Server Started listening to new connections...")
    await server.wait_closed()


if __name__ == "__main__":
    # asyncio.run() is used when running this example with Python >= 3.7v
    asyncio.run(main())
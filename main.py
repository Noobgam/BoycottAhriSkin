import asyncio
import logging

from lcu_driver import Connector
from lcu_driver.connection import Connection
from lcu_driver.events.responses import WebsocketEventResponse

# https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json
AHRI_CHAMPION_ID = 103


def main():
    connector = Connector()
    ban_lock = asyncio.Lock()

    async def try_to_ban_ahri(connection: Connection, lobby_state: dict):
        # eh. I'm not too invested into LCU to check the thread safety.
        async with ban_lock:
            my_id = lobby_state["localPlayerCellId"]

            my_active_action = None  # forced to check all, not only last
            for action in [x for el in lobby_state["actions"] for x in el]:
                if action["actorCellId"] == my_id and action["isInProgress"]:
                    my_active_action = action
                    break

            if not my_active_action:
                return

            action_id = my_active_action["id"]

            if my_active_action["type"] == "ban":
                await connection.request(
                    "patch",
                    f"/lol-champ-select/v1/session/actions/{action_id}",
                    data={"championId": AHRI_CHAMPION_ID},
                )
                await asyncio.sleep(1)
                await connection.request(
                    "post",
                    f"/lol-champ-select/v1/session/actions/{action_id}/complete",
                )
                await asyncio.sleep(1)

    @connector.ws.register(
        "/lol-champ-select/v1/session",
        event_types={
            "CREATE",
        },
    )
    async def entered_match(connection: Connection, event: WebsocketEventResponse):
        logging.info(f"Created {event.data}")

    @connector.ws.register(
        "/lol-champ-select/v1/session",
        event_types={
            "UPDATE",
        },
    )
    async def updated(connection: Connection, event: WebsocketEventResponse):
        logging.info(event.data)
        await try_to_ban_ahri(connection, event.data)

    connector.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()

from teletdd import TelegramTestClient

from app.infra.db.main import DBGateway


async def test_start_bot(
    client: TelegramTestClient, db_gateway: DBGateway
) -> None:
    await client.send_message("/start")
    messages = await client.get_response_messages()
    message = messages[0]

    user_id = (await client.get_me()).id

    user = await db_gateway.get_user(user_id)

    assert user is not None

from telethon import TelegramClient

# Prompt the user for their API_ID, API_HASH, and phone number
api_id = input("Enter your API_ID: ")
api_hash = input("Enter your API_HASH: ")
phone_number = input("Enter your phone number: ")

# Create the Telegram client
client = TelegramClient('telegram_session', api_id, api_hash)

async def main():
    # Start the client
    await client.start(phone=phone_number)

    # Get and print your own user information
    me = await client.get_me()
    print(f'Logged in as {me.first_name}')

    # Disconnect after setting up
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())

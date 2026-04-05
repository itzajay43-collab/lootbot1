from telethon import TelegramClient, events

api_id = 32985403
api_hash = "3cb0f4cb545c24c02cc332d67c38946a"

source_channel = "unboxingayush"
target_channel = "DiscountShopping40"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message.message
    
    if msg:
        await client.send_message(target_channel, msg)

client.start()
print("Bot running...")
client.run_until_disconnected()
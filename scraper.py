from telethon import TelegramClient, events
import re

# 🔑 API details
api_id = 32985403
api_hash = "3cb0f4cb545c24c02cc332d67c38946a"

# 📢 Channels
source_channel = "Online_Shopping_offers_live"
target_channel = "DiscountShopping40"

# 💰 Affiliate tag
AFFILIATE_TAG = "discountsh0b1-21"

client = TelegramClient("session", api_id, api_hash)

# ✅ Amazon link convert (multiple formats support)
def convert_amazon_link(text):
    patterns = [
        r'/dp/([A-Z0-9]{10})',
        r'/gp/product/([A-Z0-9]{10})',
        r'asin=([A-Z0-9]{10})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            pid = match.group(1)
            return f"https://www.amazon.in/dp/{pid}?tag={AFFILIATE_TAG}"
    
    return None

# ✅ Price + Discount filter
def is_good_deal(text):
    prices = re.findall(r'₹\s?(\d+)', text)
    prices = [int(p) for p in prices]

    if len(prices) >= 2:
        original = max(prices)
        deal = min(prices)

        if original == 0:
            return False

        discount = ((original - deal) / original) * 100

        # 🔥 Conditions (edit kar sakta hai)
        if discount >= 50 and deal <= 1000:
            return True

    return False

# 🤖 Message handler
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    msg = event.message.message

    if msg:
        # ❌ Filter reject
        if not is_good_deal(msg):
            return

        # 🔗 Affiliate convert
        new_link = convert_amazon_link(msg)

        # ✨ Clean message (old links remove)
        clean_msg = re.sub(r'http\S+', '', msg)

        # 📢 Final caption
        if new_link:
            final_msg = f"""🔥 *HOT DEAL ALERT* 🔥

{clean_msg}

👉 *Buy Now:* {new_link}

⏰ Limited Time Offer  
⚡ Hurry Up Fast!"""
        else:
            final_msg = clean_msg

        await client.send_message(target_channel, final_msg)

# ▶️ Run bot
client.start()
print("Bot running...")
client.run_until_disconnected()

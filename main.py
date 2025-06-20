# Web Scraper Bot - Pyrogram Version
# 🔥 By FAST Developers 🔥

import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

from scraper import (
    all_audio_scraping, all_images_scraping, all_links_scraping,
    all_paragraph_scraping, all_pdf_scraping, all_video_scraping,
    extract_cookies, extract_local_storage, html_data_scraping,
    raw_data_scraping, extract_metadata, capture_screenshot, record_screen
)
from crawler import crawl_web
from utils import OPTIONS, START_BUTTON, START_TEXT, is_verified

# Load .env variables
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
CHANNEL_USERNAME = "@FAST_Developers_Official"  # example: @FAST_Developers_Official
CRAWL_LOG_CHANNEL = os.getenv("CRAWL_LOG_CHANNEL")

if not all([bot_token, api_id, api_hash, CHANNEL_USERNAME]):
    raise ValueError("Please set BOT_TOKEN, API_ID, API_HASH, and CHANNEL_USERNAME in your .env")

# Pyrogram client
app = Client("WebScrapperBot", bot_token=bot_token, api_id=int(api_id), api_hash=api_hash)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify")]
    ])
    await message.reply("Hey 👋, Must Join given channel for Using this Bot.", reply_markup=markup)

# Handle verification & all scraping button clicks
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "verify":
        if is_verified(user_id):
            await query.answer("✅ Verified!")
            await client.send_message(
                user_id,
                "👋 Welcome to the Web Scraper Bot!\n\n"
                "Send any link to begin scraping content.\n\n"
                "🔥 *Powered by FAST Developers* 🔥",
                parse_mode="markdown"
            )
        else:
            await query.answer("❌ Please join the channel first!")

    elif data == "cbrdata":
        await raw_data_scraping(query)
    elif data == "cbhtmldata":
        await html_data_scraping(query)
    elif data == "cballlinks":
        await all_links_scraping(query)
    elif data == "cballparagraphs":
        await all_paragraph_scraping(query)
    elif data == "cballimages":
        await all_images_scraping(client, query)
    elif data == "cballaudio":
        await all_audio_scraping(client, query)
    elif data == "cballvideo":
        await all_video_scraping(client, query)
    elif data == "cballpdf":
        await all_pdf_scraping(query)
    elif data == "cbmetadata":
        await extract_metadata(query)
    elif data == "cbcookies":
        await extract_cookies(query)
    elif data == "cblocalstorage":
        await extract_local_storage(query)
    elif data == "cbscreenshot":
        await capture_screenshot(query)
    elif data == "cbscreenrecord":
        await record_screen(query)
    elif data == "cdstoptrasmission":
        await query.message.reply("🛑 Transmission Stopped.")
    elif data == "cbcrawl":
        if CRAWL_LOG_CHANNEL:
            await crawl_web(client, query)
        else:
            await query.message.reply("❌ Log Channel not set!")
    else:
        await query.message.edit_text(
            text=START_TEXT,
            disable_web_page_preview=True,
            reply_markup=START_BUTTON
        )

# Handle links from private chats
@app.on_message((filters.regex("http") | filters.regex("www")) & filters.private)
async def scrape_handler(client, message: Message):
    await message.reply_text("Choose an Option")
    await message.reply_text(
        message.text,
        reply_markup=OPTIONS,
        disable_web_page_preview=True
    )

# Run the bot
print("✅ Web Scraper Bot Running...")
app.run()

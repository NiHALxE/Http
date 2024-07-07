import asyncio
import aiohttp
import logging
from telegram import Bot
from telegram.ext import Updater 
from keep_alive import keep_alive
keep_alive()

# Define your SOCKS5 proxy settings
socks5_host = '127.0.0.1'
socks5_port = 1080
socks5_username = "NiHALx"
socks5_password = "@N2X4E"

# Define the HTTP proxy details
http_proxy_host = "rp.proxyscrape.com"
http_proxy_port = 6060
http_proxy_username = "5flsmkxrsw9o46c-country-es-session-zrwzpqf8la-lifetime-120"
http_proxy_password = "eseqv3rtarms9n9"

# Logging setup
logging.basicConfig(filename='proxy.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Telegram bot setup
telegram_token = '6746618872:AAGtr9bKxJHp9lBoFKgR4fPEkw4Ta7gTtdo'
admin_id = '6100176781'
bot = Bot(token=telegram_token)

class ProxyPool:
    def __init__(self):
        self.proxies = []

    def load_proxies(self):
        # Load your HTTP proxies here
        self.proxies.append(f'http://{http_proxy_username}:{http_proxy_password}@{http_proxy_host}:{http_proxy_port}')

    def get_proxy(self):
        # Return an available proxy from the pool
        return self.proxies[0] if self.proxies else None

async def handle_socks5_request(reader, writer):
    # Implement SOCKS5 protocol and use HTTP proxy for requests
    try:
        data = await reader.read(1024)
        target_url = 'http://example.com'  # Replace with your target URL

        proxy = proxy_pool.get_proxy()
        if proxy is None:
            writer.close()
            await writer.wait_closed()
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(target_url, proxy=proxy) as response:
                result = await response.text()
                writer.write(result.encode())
                await writer.drain()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    global proxy_pool
    proxy_pool = ProxyPool()
    proxy_pool.load_proxies()

    server = await asyncio.start_server(
        handle_socks5_request, socks5_host, socks5_port
    )

    # Send proxy details via Telegram bot
    proxy_details = f"SOCKS5 Proxy is running on {socks5_host}:{socks5_port}\n" \
                    f"Use the following SOCKS5 proxy settings in your SOCKS Droid app:\n" \
                    f"IP: {socks5_host}\nPort: {socks5_port}\nUsername: {socks5_username}\nPassword: {socks5_password}"
    bot.send_message(chat_id=admin_id, text=proxy_details)

    logging.info("SOCKS5 Proxy started")
    logging.info(proxy_details)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())

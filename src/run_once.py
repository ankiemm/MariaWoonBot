import os, sqlite3, asyncio, aiohttp, logging
from selectolax.parser import HTMLParser as Soup
from telegram import Bot

URL        = "https://www.dehuissleutel.nl/nl/aanbod"
CARD_CSS   = ".card.card--withFooter"
LINK_CSS   = "a"

TOKEN   = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

DB = sqlite3.connect("data/seen.db")
DB.execute("CREATE TABLE IF NOT EXISTS seen (url TEXT PRIMARY KEY)")

logging.basicConfig(level=logging.INFO)

async def main():
    async with aiohttp.ClientSession() as s:
        html = await (await s.get(URL, timeout=10)).text()
        soup = Soup(html)
        new_links = []
        for card in soup.css(CARD_CSS):
            a = card.css_first(LINK_CSS)
            if not a:
                continue
            url = "https://www.dehuissleutel.nl/" + a.attrs["href"].lstrip("/")
            if not DB.execute("SELECT 1 FROM seen WHERE url=?", (url,)).fetchone():
                DB.execute("INSERT INTO seen VALUES (?)", (url,))
                DB.commit()
                new_links.append(url)

        if new_links:
            text = "🏠 Nieuw op De Huissleutel:\n" + "\n".join(new_links)
            await Bot(TOKEN).send_message(chat_id=CHAT_ID, text=text)
            logging.info("Sent %d link(s)", len(new_links))
        else:
            logging.info("Geen nieuwe woningen")

if __name__ == "__main__":
    asyncio.run(main())

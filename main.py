import requests, selectolax.parser as slx
html = requests.get("https://www.dehuissleutel.nl/nl/aanbod").text
soup = slx.HTMLParser(html)

cards = soup.css(".card.card--withFooter")
print(len(cards), "kaarten gevonden")              # → bv. 6
print(cards[0].css_first("a").attrs["href"])       # → nl/woning/3803/heuvelstraat-117
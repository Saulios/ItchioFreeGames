import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()


class ItchSales:
    def __init__(self):
        games = ""
        page = 1
        while True:
            # Itch lazyloads sales, loop over all available pages
            self.url = 'https://itch.io/games/top-rated/on-sale?page=' + str(page) + '&format=json'
            self.gamePage = requests.get(
                    self.url,
                    timeout=30, verify=False)
            if self.gamePage.json()["content"] != "":
                games += self.gamePage.json()["content"]
                page += 1
            else:
                break
        self.gamepage = BeautifulSoup(games, "html.parser")
        self.freesales()

    def freesales(self):
        games = []
        sales = self.gamepage.find_all('div', {'class': 'game_cell'})
        for sale in sales:
            sale_tag = sale.find('div', {'class': 'sale_tag'})
            price_value = sale.find('div', {'class': 'price_value'})
            if price_value is not None and sale_tag.text == "-100%":
                game = sale.find('div', {'class': 'game_title'})
                title = game.find('a', {'class': 'title'})
                rating = sale.find('span', {'class': 'rating_count'})
                star_value = sale.find('div', {'class': 'star_value'})
                if hasattr(rating, 'text') and hasattr(star_value, 'text'):
                    if int(rating.text[1:-1].split()[0]) >= 3 and float(star_value.text.split()[1]) >= 4:
                        # Get the sales with at least 3 reviews and at least average 4 stars.
                        sale_to_add = {'title': title.text, 'link': title.get('href'), 'rating': float(star_value.text.split()[1]), 'total': int(rating.text[1:-1].split()[0])}
                        games.append(sale_to_add)
        # Sort by number of reviews
        games = sorted(games, key=lambda i: i['total'], reverse=True)
        for game in games:
            print("*", game['title'])
            print(game['link'])
            print("Ratings:", game['rating'], "|", game['total'])


ItchSales()

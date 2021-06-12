from urllib.parse import urlencode

import scrapy
from burplist.items import ProductItem
from burplist.utils.parsers import parse_brand, parse_quantity
from scrapy.loader import ItemLoader


class AlcohaulSpider(scrapy.Spider):
    """
    Parse data from site's API
    """
    name = 'alcohaul'
    BASE_URL = 'https://alcohaul.sg/api/productlist?'

    params = {
        'skip': 0,
        'limit': 50,
        'parent': '5f7edae59ae56e6d7b8b456d',
        'filter': 'a-z',
        'child': '5f7edb459ae56e6d7b8b45df',
    }

    def start_requests(self):
        url = self.BASE_URL + urlencode(self.params)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        products = data['items']

        if products:
            for product in products:
                if product['quantity'] < 1:
                    # Skipping products which are out of stock
                    continue

                loader = ItemLoader(item=ProductItem())
                slug = product['slug']

                loader.add_value('platform', self.name)

                loader.add_value('name', product['name'])
                loader.add_value('url', f'https://alcohaul.sg/products/{slug}')

                loader.add_value('brand', parse_brand(product['name']))
                loader.add_value('origin', product.get('country'))
                loader.add_value('style', product.get('type'))

                loader.add_value('abv', product.get('alcohol'))
                loader.add_value('volume', product['name'])
                loader.add_value('quantity', parse_quantity(product['name']))

                loader.add_value('price', str(product['smartPrice']))

                yield loader.load_item()

            self.params['skip'] += 50
            next_page = self.BASE_URL + urlencode(self.params)
            yield response.follow(next_page, callback=self.parse)

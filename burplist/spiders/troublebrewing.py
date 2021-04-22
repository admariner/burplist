import json
import re
from typing import Optional

import scrapy
from burplist.items import ProductItem
from scrapy.loader import ItemLoader


class TroubleBrewingSpider(scrapy.Spider):
    """
    Extract data from raw HTML
    Starting URL is from a base URL which contains collections of beers, we then need to dive into each individual collection URL to obtain the product information

    We get the beer information via a html script tag as shown in the example below:
    <script>
    ...
    var meta = {"product":{"id":4468579795059,"gid":"gid://shopify/Product/4468579795059","vendor":"Trouble Brewing Store","type":"Beer","variants":[{"id":31829208989811,"price":7700,"name":"Middle Child Wheat Beer - 24 pack","public_title":"24 pack","sku":"TCWB24B"},{"id":32061886857331,"price":4200,"name":"Middle Child Wheat Beer - 12 pack","public_title":"12 pack","sku":"TCWB12B"},{"id":31829224194163,"price":2200,"name":"Middle Child Wheat Beer - 6 pack","public_title":"6 pack","sku":"TCWB6B"}]},"page":{"pageType":"product","resourceType":"product","resourceId":4468579795059},"page_view_event_id":"9e681da76f7007fc67a3a5a2fee2501bba0089fc71f880ef6fe820cce2fce5ee","cart_event_id":"34099f8e9fac4792e8758a189e2bda70923c0d854dc4067398d5a7b104e4a719"};
    ...
    </script>
    """
    name = 'troublebrewing'
    start_urls = ['https://troublebrewing.com/collections/trouble-beer-cider-hard-seltzer']

    def _get_product_quantity(self, sku: str, public_title: Optional[str] = None) -> int:
        # Special case for "Trouble Brewing x @FEEDBENG Chinese New Year Gift Set"
        if public_title and 'Gift Set' in public_title:
            return 2

        if sku.endswith('24B'):
            return 24
        if sku.endswith('12B'):
            return 12
        if sku.endswith('6B'):
            return 6
        if sku.startswith('SGBN') or sku.startswith('TCMX') or sku == '':
            return 24
        return 1

    def parse(self, response):
        collections = response.xpath('//a[@class="product-link js-product-link"]/@href')

        for collection in collections:
            url = response.urljoin(collection.get())
            yield scrapy.Request(url=url, callback=self.parse_collection)

    def parse_collection(self, response):
        script_tag = response.xpath('//script[contains(.,"var meta")]/text()').get()
        data = re.search(r'\[\{(.*?)\]', script_tag).group()
        products = json.loads(data)

        for product in products:
            loader = ItemLoader(item=ProductItem())
            loader.add_value('name', product['name'].split('-', maxsplit=2)[0])
            loader.add_value('vendor', self.name)
            loader.add_value('price', str(product['price'] / 100))  # E.g.: 7700 == $77.00
            loader.add_value('quantity', self._get_product_quantity(product['sku'], product['public_title']))
            loader.add_value('url', response.request.url)
            yield loader.load_item()

import re

import scrapy
from burplist.items import ProductLoader


class CraftBeerSGSpider(scrapy.Spider):
    """Parse data from raw HTML

    Product quantity may be "Pack of 6", "Pack of 16", "Pack of 24", and etc.
    This spider passes ProductItem into nested request

    # TODO: Extract `origin` information
    # TODO: Add contracts to `parse_collection`. Need to handle passing of `meta`
    """

    name = 'craftbeersg'
    start_urls = ['https://craftbeersg.com/product-category/beer/by-brewery/']

    def parse(self, response):
        """
        @url https://craftbeersg.com/product-category/beer/by-brewery/
        @returns requests 1
        """
        collections = response.xpath('//li[@class="cat-item cat-item-145 current-cat cat-parent"]//li/a')
        for collection in collections:
            brand = collection.xpath('./text()').get()
            yield response.follow(collection, callback=self.parse_collection, meta={'brand': brand})

    def parse_collection(self, response):
        products = response.xpath('//div[@class="product-inner"]')

        brand = response.meta['brand']

        for product in products:
            loader = ProductLoader(selector=product)
            loader.add_value('platform', self.name)

            raw_name = product.xpath('.//a[@class="product-loop-title"]/h3/text()').get()
            name, quantity = self.get_product_name_quantity(raw_name)

            loader.add_value('name', name)

            url = response.urljoin(product.xpath('.//a[@class="product-loop-title"]/@href').get())
            loader.add_value('url', url)

            loader.add_value('brand', brand)
            loader.add_value('origin', None)
            loader.add_value('quantity', quantity)

            loader.add_xpath('price', './/span[@class="woocommerce-Price-amount amount"]//bdi/text()')

            yield scrapy.Request(
                url,
                callback=self.parse_product_detail,
                meta={'item': loader.load_item()},
                dont_filter=False,
            )

        # Recursively follow the link to the next page, extracting data from it
        next_page = response.css('a.next.page-numbers').attrib.get('href')
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product_detail(self, response):
        loadernext = ProductLoader(item=response.meta['item'], response=response)

        raw_description = response.xpath('.//div[@class="description woocommerce-product-details__short-description"]//text()').getall()
        raw_description_list = ''.join(raw_description).split('\n')  # NOTE: To workaround case where the style, volume, and abv are separate element in an array

        descriptions = next((string for string in raw_description_list if '|' in string), '|')

        attributes = descriptions.split('|')
        if len(attributes) == 2:  # "330ml | 4.8% ABV"
            style = None
            volume, abv = attributes

        else:  # "Cider | 330ml | ABV 4%"
            style, volume, abv = attributes

        loadernext.add_value('style', style)
        loadernext.add_value('volume', volume)
        loadernext.add_value('abv', abv)

        image_url = response.xpath('//div[@class="img-thumbnail"]//img/@src').get()
        loadernext.add_value('image_url', image_url)

        yield loadernext.load_item()

    @staticmethod
    def get_product_name_quantity(raw_name: str) -> tuple[str, int]:
        parsed_name = raw_name.split('~', maxsplit=2)  # "Magic Rock Brewing. Fantasma Gluten Free IPA ~ P198"
        name = re.sub('[()]', '', parsed_name[0])

        if 'Pack of' in name:
            name, quantity = name.split('Pack of', maxsplit=2)
            return name, int(quantity)

        if 'Case of' in name:
            name, quantity = name.split('Case of', maxsplit=2)
            return name, int(quantity)

        return name, 1

import logging
import os
import re

import scrapy
from burplist.items import ProductItem
from scrapy.downloadermiddlewares.retry import get_retry_request
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)

settings = get_project_settings()


class RedMartSpider(scrapy.Spider):
    """
    Parse data from site's API
    The API structure is similar to Lazada

    - https://redmart.lazada.sg/shop-beer/?from=rm_nav_cate&m=redmart&rating=4
    - https://redmart.lazada.sg/shop-groceries-winesbeersspirits-beer-craftspecialtybeer/?from=rm_nav_cate&m=redmart&rating=4
    """
    name = 'redmart'
    custom_settings = {
        'DOWNLOAD_DELAY': os.environ.get('REDMART_DOWNLOAD_DELAY', 60),
        'DOWNLOADER_MIDDLEWARES': {
            **settings.get('DOWNLOADER_MIDDLEWARES'),
            'burplist.middlewares.DelayedRequestsMiddleware': 100,
        },
    }

    start_urls = [
        f'https://redmart.lazada.sg/shop-groceries-winesbeersspirits-beer-craftspecialtybeer/?ajax=true&from=rm_nav_cate&m=redmart&page={n}&rating=4'
        for n in range(1, 6)
    ] + [
        f'https://redmart.lazada.sg/shop-beer/?ajax=true&from=rm_nav_cate&m=redmart&page={n}&rating=4'
        for n in range(1, 6)
    ]

    def _get_product_quantity(self, package_info: str) -> int:
        raw_quantity = re.split('×', package_info)  # E.g.: "40 × 320 ml", "330 ml"

        if len(raw_quantity) > 1:
            return int(raw_quantity[0])

        return 1

    def parse(self, response):
        logger.info(response.request.headers)
        data = response.json()
        if 'rgv587_flag' in data:
            error = f'Rate limited by Red Mart. URL <{response.request.url}>.'
            logger.warning(error)

            retry_request = get_retry_request(response.request, reason=error, spider=self)
            if retry_request:
                yield retry_request
            return

        products = data['mods']['listItems']

        # Stop sending requests when the REST API returns an empty array
        if products:
            for product in products:
                loader = ItemLoader(item=ProductItem(), selector=product)

                loader.add_value('vendor', self.name)
                loader.add_value('name', product['name'])
                loader.add_value('price', product['price'])
                loader.add_value('quantity', self._get_product_quantity(product['packageInfo']))
                loader.add_value('url', product['productUrl'].replace('//', ''))
                yield loader.load_item()

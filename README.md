# Burplist

The goal here is to aggregate all the available beer (preferably craft beer) data in Singapore into a single location

## Start Crawling

### Without Proxy (For Development)

```sh
# Omit `-o filename.json` if you do not want to generate the output in json
pipenv run scrapy crawl alcoholdelivery -o alcoholdelivery.json
pipenv run scrapy crawl beerforce -o beerforce.json
pipenv run scrapy crawl coldstorage -o coldstorage.json
pipenv run scrapy crawl craftbeersg -o craftbeersg.json
pipenv run scrapy crawl fairprice -o fairprice.json
pipenv run scrapy crawl thirsty -o thristy.json --set=ROBOTSTXT_OBEY='False'
```

### Using Proxy (For Production)

```sh
export SCRAPER_API_KEY="YOUR_SCRAPER_API_KEY"
pipenv run scrapy crawl craftbeersg -o craftbeersg.json --set=ROBOTSTXT_OBEY='False'
```

## Database Schema

https://dbdiagram.io/d/605d3ad2ecb54e10c33d5165

## Scrapy Tools and Libraries

https://github.com/croqaz/awesome-scrapy

## Item Loader

https://towardsdatascience.com/demystifying-scrapy-item-loaders-ffbc119d592a

## Unit Testing

https://stackoverflow.com/questions/6456304/scrapy-unit-testing

```sh
pipenv run python3 -m unittest
```

## Bulk Insert in SQLAlchemy

[I’m inserting 400,000 rows with the ORM and it’s really slow!](https://docs.sqlalchemy.org/en/13/faq/performance.html#i-m-inserting-400-000-rows-with-the-orm-and-it-s-really-slow)

https://stackoverflow.com/questions/36386359/sqlalchemy-bulk-insert-with-one-to-one-relation

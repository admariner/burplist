# Development, Debug and Troubleshoot

## Database Set Up

For local development:

```sh
# To spin up a PostgreSQL Docker container
docker run -d --name dpostgres -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres:latest

# To run `psql` in the Docker container
docker exec -it dpostgres psql -U postgres
```

## XPath Quick Guide

> “XPath is a language for addressing parts of an XML document”

It is highly recommended to read these materials about XPath, it will save you a lot of time:

-   https://dev.to/masihurmaruf/locator-strategy-xpath-54p7
-   https://docs.scrapy.org/en/xpath-tutorial/topics/xpath-tutorial.html

## Selecting Dynamically-loaded Content

References:

-   https://docs.scrapy.org/en/latest/topics/dynamic-content.html
-   https://www.zyte.com/blog/handling-javascript-in-scrapy-with-splash/

```sh
docker run -d -p 8050:8050 scrapinghub/splash
```

### Using `scrapy-splash` with `scrapy shell`

```sh
pipenv run scrapy shell 'http://localhost:8050/render.html?url=https://www.alcoholdelivery.com.sg/beer-cider/craft-beer'
```

### Check if site loads content dynamically with JavaScript

You can inspect your browser and `Cmd + Shift + P` to `> Disable JavaScript` to check if the page loads using JavaScript.

```sh
pipenv run scrapy view https://coldstorage.com.sg/beers-wines-spirits/beer-cidercraft-beers
```

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

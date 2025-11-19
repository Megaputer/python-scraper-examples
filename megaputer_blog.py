"""
### Megaputer blog scraper

Downloads articles from https://megaputer.com/blog

#### Columns

| Name        | Type      | Description
| :---------- | :-------- | :----------
| `Published` | Date/Time | Publication date

"""
import logging
from datetime import datetime

import lxml.html
import requests

from utils import column_types, default_datetime_format, InternetNode


def main():
    columns = {'Published': column_types['Date/Time']}
    with InternetNode(__doc__, columns) as node, requests.Session() as s:

        # walk through blog pages and collect post links
        url = 'https://megaputer.com/blog'
        posts = {}
        while True:
            if node.is_cancelled():
                logging.info('Node execution is cancelled')
                return

            with s.get(url) as resp:
                resp.raise_for_status()
                dom = lxml.html.fromstring(resp.content)

            for article_el in dom.xpath('//article'):
                link = article_el.xpath('.//a[@rel="bookmark"]/@href')[0]
                _published = article_el.xpath('.//time/@datetime')[0]

                # convert @datetime format to PA: '2020-12-10 12:00:54' > '12/10/2020 01:00:54 pm'
                _parsed = datetime.strptime(_published, '%Y-%m-%d %H:%M:%S')
                published = _parsed.strftime(default_datetime_format)
                posts[link] = published

            try:
                url = dom.xpath('//nav//a[contains(@class, "next")]/@href')[0]
            except IndexError:
                logging.info(f'Theres no more pages {url}')
                break

        logging.info(f'Found next blog posts: {posts}')
        # download collected posts
        c = 0
        for url, published in posts.items():
            if node.is_cancelled() or c >= node.rows_limit:
                logging.info('Node execution is cancelled')
                break

            try:
                with s.get(url) as resp:
                    resp.raise_for_status()
                    dom = lxml.html.fromstring(resp.content)

                texts = dom.xpath('//main/section[contains(@class,"l-section") and not(contains(@class, "for_sharing")) and not(contains(@class, "for_related"))]//text()')

                try:
                    title = dom.xpath('//title/text()')[0].strip()
                except (IndexError, AttributeError):
                    title = ''

            except Exception as exc:
                logging.warning(f'Failed to download post "{url}": {exc}')
                continue

            node.insert(url, title, ''.join(texts), Published=published)
            c += 1


if __name__ == '__main__':
    main()

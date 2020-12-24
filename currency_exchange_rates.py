"""
### Get latest currency exchange rates based on EUR
"""
import lxml.html
import requests

from utils import column_types, InternetNode

# todo use parametric columns


def main():
    with InternetNode(__doc__, columns={'Rate': column_types['Numerical']}) as node:
        node.bulk_size = 100  # insert all rates at once

        resp = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        dom = lxml.html.fromstring(resp.content)

        for el in dom.xpath('//cube[@rate]'):
            node.insert(
                url=el.get('currency'),
                Rate=el.get('rate')
            )


if __name__ == '__main__':
    main()

import argparse
import base64
import configparser
import json


class FileAction(argparse.Action):
    """Custom argparse action.

    Used to write scraper description and features to the file.
    """

    def __init__(self, option_strings, text='', nargs=None, help=None, **_):
        super().__init__(
            option_strings=option_strings,
            dest=argparse.SUPPRESS,
            nargs=nargs,
            const=None,
            default=argparse.SUPPRESS,
            type=argparse.FileType(mode='w', encoding='utf_8'),
            choices=None,
            required=False,
            help=help,
            metavar='FILE',
        )
        self.text = text

    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            values.write(self.text)
            values.close()
        else:
            parser.print_help()
        parser.exit()


def parse_arguments(description='', features=''):
    """Parse command-line arguments and return configuration file object."""
    parser = argparse.ArgumentParser(add_help=False, description=description)
    parser.add_argument(
        'conf',
        metavar='FILE',
        help='configuration file',
        type=argparse.FileType(mode='r', encoding='utf_8'),
    )
    parser.add_argument(
        '-h',
        '--help',
        action=FileAction,
        text=description,
        nargs='?',
        help='write scraper description to the file and exit if value supplied\
        otherwise show this help message and exit',
    )
    parser.add_argument(
        '--features',
        action=FileAction,
        text=features,
        help='write scraper features to the file and exit',
    )
    return parser.parse_args().conf


DataTypes = {
    'bool': '$bool',
    'str': '$cat_string',
    'num': '$num',
    'datetime': '$num_datetime'
}


def features(ini, **kwargs):
    return json.dumps(
        {
            'columns': [{'name': k, 'type': v} for k, v in kwargs.items()],
            'params': ini
        },
        indent=4
    )


def parse_ini(ini):
    """Converts ini file string to dict."""
    configparser.ConfigParser.optionxform = str  # make parser case insensitive
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read_string(ini)

    return {k: v for k, v in parser['DEFAULT'].items()}


def write(path, url, content, title, **kwargs):
    encoded = base64.standard_b64encode(content).decode('ascii')

    with open(path, mode='w', encoding='utf_8') as f:
        data = {
            'docs': [
                {
                    'url': url,
                    'docurl': url,
                    'title': title,
                    'mime': 'text/html',
                    'content': encoded,
                    'columns': kwargs,
                    'files': {},
                }
            ]
        }
        json.dump(data, f, indent=4)


def main(data):
    write(
        data['output_folder'] + '\example_result.json',
        'http://example.com',
        'Example text content'.encode('utf_8'),
        'Example title',
    )


if __name__ == '__main__':
    descr = 'web scraper template'
    file = parse_arguments(descr, features(''))

    data = json.loads(file.read())
    data['params'] = parse_ini(data['params'])

    main(data)

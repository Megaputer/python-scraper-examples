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


def get_features(params, **kwargs):
    """Returns string in PolyAnalyst's json format."""
    return json.dumps(
        {
            'columns': [{'name': k, 'type': v} for k, v in kwargs.items()],
            'params': params
        }
    )


def parse_ini(ini):
    """Returns keys from default section of ini file as a dict."""
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.optionxform = str  # make parser case-sensitive
    parser.read_string(ini)

    return dict(parser['DEFAULT'])


# dict of Internet Source's supported data types
DataTypes = {
    'bool': '$bool',
    'str': '$cat_string',
    'num': '$num',
    'datetime': '$num_datetime'
}


def write(path, url, content, title, **kwargs):
    """Writes json file with PolyAnalyst's result format."""
    data = {
        'docs': [
            {
                'url': url,
                'docurl': url,
                'title': title,
                'mime': 'text/html',
                'content': base64.standard_b64encode(content).decode('ascii'),
                'columns': kwargs,
                'files': {},
            }
        ]
    }

    with open(path, mode='w', encoding='utf_8') as f:
        json.dump(data, f)


def main(data):
    write(
        path=data['output_folder'] + '\example_result.json',
        url='http://example.com',
        content=b'Example text content',
        title='Example title',
        ExtraColumn=data['params']['value_for_ExtraColumn'],
    )


if __name__ == '__main__':
    description = 'web scraper template'
    ini = '[DEFAULT]\nvalue_for_ExtraColumn=default value'
    features = get_features(ini, ExtraColumn=DataTypes['str'])
    file = parse_arguments(description, features)

    data = json.load(file)
    data['params'] = parse_ini(data['params'])

    main(data)

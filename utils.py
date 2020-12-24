import argparse
import base64
import configparser
import io
import json
import logging
import math
import pathlib
import sys
import uuid

__all__ = ['column_types', 'default_datetime_format', 'InternetNode']

# todo parametric columns

column_types = {
    'Numerical':  '$num',
    'Integer':    '$num_int',
    'Boolean':    '$bool',
    'String':     '$cat_string',
    'Date/Time':  '$num_datetime',
    'String ID':  '$cat',
    'Integer ID': '$id',
    'Text':       '$text',
}
default_datetime_format = '%m/%d/%Y %I:%M:%S %p'


class INI:
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.optionxform = str  # make option names case sensitive

    @classmethod
    def dumps(cls, d):
        """Serialize `d` (a `dict`) to a INI file formatted `str`"""
        cls.parser['DEFAULT'] = d
        buf = io.StringIO()
        cls.parser.write(buf)
        buf.seek(0)
        return buf.read()

    @classmethod
    def loads(cls, s):
        """Deserialize `s` (a `str` instance containing an INI file content) to a `dict`"""
        cls.parser.read_string(s)
        return dict(cls.parser['DEFAULT'])


class WriteTextOrPrintHelp(argparse.Action):
    """Custom action to write scraper description and features to the file"""

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


def _parse_arguments(description, features):
    """Parse command-line arguments and return configuration file object"""
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
        action=WriteTextOrPrintHelp,
        text=description,
        nargs='?',
        help='write scraper description to the file and exit if file path supplied\
        otherwise show this help message and exit',
    )
    parser.add_argument(
        '--features',
        action=WriteTextOrPrintHelp,
        text=features,
        help='write scraper features to the file and exit',
    )
    return parser.parse_args().conf


class InternetNode:
    """
    Simple abstraction over PolyAnalyst and external scraper interactions

    :param description: (optional) Scraper description and usage for end user (in markdown)
    :param columns: (optional) Define additional columns with (column_name: column_type) mapping
    :param parameters: (optional) Define parameters with (name: value) mapping

    Usage::
      >>> with InternetNode(description='Simplest scraper example') as node
      >>>     node.insert('https://example.com', 'Example title', 'Lorem ipsum')
    """

    serializer = INI

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
        logging.error('An unhandled error occurred in scraper:', exc_info=True)

    def __init__(self, description='', columns=None, parameters=None):
        if columns is None:
            columns = {}
        if parameters is None:
            parameters = {}

        features = json.dumps({
            'columns': [{'name': k, 'type': v} for k, v in columns.items()],
            'params': self.serializer.dumps(parameters),
        })
        cfg = json.load(_parse_arguments(description, features))

        self.url = cfg['url']
        self.rows_limit = cfg['maximum_rows'] or math.inf
        self.parameters = self.serializer.loads(cfg['params'])
        self._output_dir = pathlib.Path(cfg['output_folder'])
        self._log_dir = pathlib.Path(cfg['log_folder'])
        self.is_debug = cfg['debug_mode']
        # todo self.proxy and self.no_proxy

        self._setup_logging()
        self._buffer = []
        self.bulk_size = 10

    def _setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG if self.is_debug else logging.INFO)

        handler = logging.FileHandler(
            self._log_dir / f'{pathlib.Path(sys.argv[0]).stem}_{uuid.uuid4().hex}.log',
            encoding='utf-8'
        )
        handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s.%(msecs)3d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
            )
        )
        logger.addHandler(handler)

    def insert(self, url: str, title='', content=' ', **additional_columns):
        """
        Insert the row to node's dataset.

        :param url: The link to the web page. Must be unique.
        :param title: (optional) The title of web page
        :param content: (optional) The content of web page. Must not be emtpy.
        :param additional_columns: (optional) (additional_column_name: content) mapping

        Note that the rows are inserted in bulk (the size of bulk defined by bulk_size attribute).
        So the current row is not always inserted immediately to node's dataset. To insert rows
        one by one either set `bulk_size` to 1 or call `flush` after each `insert`.
        """
        if isinstance(content, str):
            content = content.encode()
        self._buffer.append({
            'docurl': url,
            'title': title,
            'content': base64.standard_b64encode(content).decode('ascii'),
            'columns': additional_columns,
        })
        if len(self._buffer) >= self.bulk_size:
            self.flush()

    def flush(self):
        """ Flush rows from buffer to PolyAnalyst """
        _buffer, self._buffer = self._buffer, []
        _file = self._output_dir / uuid.uuid4().hex
        lockfile = _file.with_suffix('.lock')
        try:
            lockfile.touch()
            with open(_file, mode='w', encoding='utf_8') as f:
                json.dump({'docs': _buffer}, f)
        except Exception as exc:
            logging.warning(f'Failed to insert rows because of: {exc}')
        finally:
            lockfile.unlink(missing_ok=True)

    def is_cancelled(self):
        """ Check that the node execution is cancelled """
        return (self._output_dir / 'STOP').is_file()

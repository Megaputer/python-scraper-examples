.. python-scraper-template documentation master file, created by
   sphinx-quickstart on Fri Jul 13 11:21:47 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to python-scraper-template's documentation!
===================================================

scraper-template.py contains set of classes, functions and objects that describes formats and
simplifies web scraper writing for PolyAnalyst's Internet Source node.

Examples
^^^^^^^^

Write static record::

   conf_file = parse_arguments('', get_features(''))
   data = json.load(conf_file)

   write(
       path=data['output_folder'] + '\example_result.json',
       url='http://www.example.com',
       content=b'Example text content',
       title='Example title'
   )

Fetch an url and write::

   import requests
   import lxml.html

   conf_file = parse_arguments('', get_features(''))
   data = json.load(conf_file)

   response = requests.get(data['url'])
   dom = lxml.html.fromstring(response.text)
   title = dom.xpath('//title/text()')[0].strip()

   write(
       path=data['output_folder'] + '\example_result.json',
       url=data['url'],
       content=response.content,
       title=title
   )

*Parameters* and *extra column* usage::

   # get 'the_answer' value from 'Parameters' and write it as a value of
   # 'Answer' extra column

   ini = '[DEFAULT]\nthe_answer=42'
   # define an Parameters string, extra column name and type
   features = get_features(ini, Answer=DataTypes['num'])

   conf_file = parse_arguments(ini, features)
   data = json.load(conf_file)

   try:
       the_answer= data['params']['the_answer']
       the_answer = float(the_answer)
   except (KeyError, ValueError):
       the_answer = 42  # set default on error

   write(
       path=data['output_folder'] + '\example_result.json',
       url='',
       content=b' ',
       title='',
       Answer=the_answer
   )

API Reference
^^^^^^^^^^^^^

.. data:: DataTypes

   The dictionary of the supported column data types:

   ======== ============= =======================================================
   key      value         description
   ======== ============= =======================================================
   bool     $bool         boolean type
   str      $cat_string   string type
   num      $num          number with a floating point
   datetime $num_datetime date/time type. The format depends on the user settings
   ======== ============= =======================================================

.. class:: FileAction(option_strings, text='', nargs=None, help=None, **_)

   Custom argparse action. Used to write scraper description and features to the file.

   See other parameters: `argparse.Action parameters <https://docs.python.org/3/library/argparse.html#argparse.Action>`_.

   :param str text: (optional) The text content of file.

.. function:: parse_arguments(description='', features='')

   The function defines the arguments required to work with PolyAnalyst's Internet Source node
   and parses them.

   :param str description: The description of what the scraper does and how it works.
   :param str features: The output of :func:`get_features<get_features>` function.
   :return: PolyAnalyst's configuration `file object <https://docs.python.org/3/glossary.html#term-file-object>`_.
   :rtype: io.TextIOWrapper

.. function:: get_features(params, **kwargs)

   Dumps arguments to a json formatted string with specific format.

   :param str params: A multiline string, which will be displayed in Parameters textbox.
   :param \**kwargs: Extra column name and type keyword arguments.
   :return: A string in PolyAnalyst's format.
   :rtype: str

   :math: `A_\text{c} = (\pi/4) d^2`.

.. note:: This is a note.
   This is the second line

   - The note contains
   - It includes.

   Usage::

     >>> ini = '[DEFAULT]\nauthor='
     >>> get_features(params=ini, Author=DataTypes['str'])
     '{"columns": [{"name": "Author", "type": "$cat_string"}], "params": "[DEFAULT]\\nauthor="}'

.. function:: parse_ini(ini)

   Parses ini argument as an ini file format and returns keys from default section of ini file as a dict.
   Parser are case-sensitive and allows keys with no values.

   :param str ini: A valid ini string.
   :return: The dictionary object with keys from default section of ini argument.
   :rtype: dict

   Usage::

     >>> ini = "[DEFAULT]\nOne=\none=1"
     >>> print(parse_ini(ini))
     {'One': '', 'one': '1'}

.. function:: write(path, url, content, title, **kwargs)

   The function dumps arguments to a specific json format and writes to *path* file.
   See usage examples in `Examples`_ section.

   :param str path: The pathname of the output file.
   :param str url: Url of the resource, will be displayed under *URL* column.
   :param bytes content: Encoded string, will be displayed under *Text content* column.
   :param str title: Title of the resource, will be displayed under 'Title' column.
   :param \**kwargs: Extra column name and value keyword arguments.

   :return: None

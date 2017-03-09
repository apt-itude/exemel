"""Converts a dictionary into an XML document"""

import collections

from future.utils import iteritems
from lxml import etree


class Error(Exception):

    """Base exception class for exemel errors"""


def build(dictionary, root='root', encoding=None):
    """Builds an XML element from a dictionary-like object

    Args:
        dictionary (collections.Mapping): The structure to be converted

    Keyword Args:
        root (string):     The tag of the root element. Defaults to 'root'.

        encoding (string): The encoding of the resulting string. Defaults to
                           a byte string.

    Returns:
        string: An XML element built from the given data structure
    """
    element = _build_element_from_dict(root, dictionary)

    return etree.tostring(element, encoding=encoding)


def build_element(dictionary, root='root'):
    """Builds an XML element from a dictionary-like object

    Args:
        dictionary (collections.Mapping): The structure to be converted

    Keyword Args:
        root (string): The tag of the root element. Defaults to 'root'.

    Returns:
        lxml.etree._Element: An XML element built from the given data structure
    """
    return _build_element_from_dict(root, dictionary)


def _build_element_from_dict(name, dictionary, parent_namespace=None):
    try:
        namespace = dictionary['#ns']
    except KeyError:
        namespace = parent_namespace

    tag = _make_tag(name, namespace)
    element = etree.Element(tag)

    for key, value in _iter_items_except_namespace(dictionary):
        if key.startswith('@'):
            _set_attribute(element, key[1:], value)
        elif key == '#text':
            _set_text(element, value)
        else:
            _add_sub_elements(element, key, value, namespace)

    return element


def _make_tag(name, namespace):
    return name if namespace is None else etree.QName(namespace, name)


def _iter_items_except_namespace(dictionary):
    for key, value in iteritems(dictionary):
        if key != '#ns':
            yield key, value


def _set_attribute(element, name, value):
    if value is not None:
        element.set(name, _convert_to_text(value))


def _set_text(element, value):
    if value is not None:
        element.text = _convert_to_text(value)


def _add_sub_elements(element, name, value, namespace):
    if etree.iselement(value):
        _validate_element_name(value, name)
        element.append(value)
    elif isinstance(value, collections.Mapping):
        element.append(_build_element_from_dict(name, value, namespace))
    elif (isinstance(value, collections.Iterable) and
          not isinstance(value, str)):
        for sub_elem in _build_elements_from_iterable(name, value, namespace):
            element.append(sub_elem)
    else:
        element.append(_build_element_from_value(name, value, namespace))


def _build_elements_from_iterable(name, iterable, parent_namespace):
    for item in iterable:
        if etree.iselement(item):
            _validate_element_name(item, name)
            element = item
        elif isinstance(item, collections.Mapping):
            element = _build_element_from_dict(name, item, parent_namespace)
        else:
            element = _build_element_from_value(name, item, parent_namespace)

        yield element


def _build_element_from_value(name, value, parent_namespace):
    tag = _make_tag(name, parent_namespace)
    element = etree.Element(tag)
    _set_text(element, value)
    return element


def _convert_to_text(value):
    if isinstance(value, bool):
        text = 'true' if value else 'false'
    else:
        text = str(value)

    return text


def _validate_element_name(element, expected_name):
    actual_name = etree.QName(element.tag).localname
    if actual_name != expected_name:
        raise MismatchedElementNameError(expected_name, actual_name)


class MismatchedElementNameError(Error):

    def __init__(self, expected_name, actual_name):
        super(MismatchedElementNameError, self).__init__(
            "Element with name '{}' was added where name '{}' was "
            "expected".format(actual_name, expected_name))

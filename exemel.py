"""Converts a dictionary into an XML document"""

import collections

from lxml import etree


def build(dictionary, root='root'):
    """Builds an XML document from a dictionary-like object

    Args:
        dictionary (collections.Mapping): The structure to be converted

    Keyword Args:
        root (string): The tag of the root element. Defaults to 'root'.

    Returns:
        string: An XML document built from the given data structure
    """
    element = _build_element_from_dict(root, dictionary)

    return etree.tostring(element)


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
    for key, value in dictionary.iteritems():
        if key != '#ns':
            yield key, value


def _set_attribute(element, name, value):
    if value is not None:
        element.set(name, _convert_to_text(value))


def _set_text(element, value):
    if value is not None:
        element.text = _convert_to_text(value)


def _add_sub_elements(element, name, value, namespace):
    if isinstance(value, collections.Mapping):
        element.append(_build_element_from_dict(name, value, namespace))
    elif (isinstance(value, collections.Iterable) and
          not isinstance(value, basestring)):
        for sub_elem in _build_elements_from_iterable(name, value, namespace):
            element.append(sub_elem)
    else:
        element.append(_build_element_from_value(name, value, namespace))


def _build_elements_from_iterable(name, iterable, parent_namespace):
    for item in iterable:
        if isinstance(item, collections.Mapping):
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

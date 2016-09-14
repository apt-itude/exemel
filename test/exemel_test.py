"""Unit tests for the exemel module"""

import collections
import unittest

from lxml import etree
import xmlunittest

import exemel


class RootElementTestCase(xmlunittest.XmlTestCase):

    def test_default_root(self):
        actual_xml = exemel.build({})

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_custom_root(self):
        actual_xml = exemel.build({}, root='custom')

        expected_xml = '<custom/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class DictTestCase(xmlunittest.XmlTestCase):

    def test_root_is_empty_dict(self):
        actual_xml = exemel.build({})

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_keys_become_sub_elements(self):
        dictionary = collections.OrderedDict()
        dictionary['alpha'] = 'a'
        dictionary['bravo'] = 'b'

        actual_xml = exemel.build(dictionary)

        expected_xml = """
            <root>
                <alpha>a</alpha>
                <bravo>b</bravo>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_sub_element_is_empty_dict(self):
        actual_xml = exemel.build({
            'alpha': {}
        })

        expected_xml = """
            <root>
                <alpha/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class TypesTestCase(xmlunittest.XmlTestCase):

    def test_none_value(self):
        actual_xml = exemel.build({
            'alpha': None,
        })

        expected_xml = """
            <root>
                <alpha/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_int_value(self):
        actual_xml = exemel.build({
            'alpha': 0,
        })

        expected_xml = """
            <root>
                <alpha>0</alpha>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_float_value(self):
        actual_xml = exemel.build({
            'alpha': 1.1,
        })

        expected_xml = """
            <root>
                <alpha>1.1</alpha>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_boolean_values(self):
        dictionary = collections.OrderedDict()
        dictionary['alpha'] = True
        dictionary['bravo'] = False

        actual_xml = exemel.build(dictionary)

        expected_xml = """
            <root>
                <alpha>true</alpha>
                <bravo>false</bravo>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class ListTestCase(xmlunittest.XmlTestCase):

    def test_empty_list(self):
        actual_xml = exemel.build({
            'myList': []
        })

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_value_items(self):
        actual_xml = exemel.build({
            'myList': ['foo', 0, 1.1, True, False, None]
        })

        expected_xml = """
            <root>
                <myList>foo</myList>
                <myList>0</myList>
                <myList>1.1</myList>
                <myList>true</myList>
                <myList>false</myList>
                <myList/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_dict_items(self):
        item1 = collections.OrderedDict()
        item1['alpha'] = 0
        item1['bravo'] = 1

        item2 = collections.OrderedDict()
        item2['alpha'] = 2
        item2['bravo'] = 3

        actual_xml = exemel.build({
            'myList': [item1, item2]
        })

        expected_xml = """
            <root>
                <myList>
                    <alpha>0</alpha>
                    <bravo>1</bravo>
                </myList>
                <myList>
                    <alpha>2</alpha>
                    <bravo>3</bravo>
                </myList>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class EtreeElementTestCase(xmlunittest.XmlTestCase):

    def setUp(self):
        tag = etree.QName('test:ns', 'existing-element')
        self.existing_element = etree.Element(tag)
        self.existing_element.text = 'test-value'

    def test_in_dict_matching_name(self):

        actual_xml = exemel.build({
            'existing-element': self.existing_element
        })

        expected_xml = """
            <root>
                <existing-element xmlns="test:ns">test-value</existing-element>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_in_dict_mismatched_name(self):
        with self.assertRaises(exemel.MismatchedElementNameError):
            exemel.build({
                'mismatched-name': self.existing_element
            })

    def test_in_list_matching_name(self):
        actual_xml = exemel.build({
            'existing-element': [
                'foo',
                self.existing_element,
                'bar'
            ]
        })

        expected_xml = """
            <root>
                <existing-element>foo</existing-element>
                <existing-element xmlns="test:ns">test-value</existing-element>
                <existing-element>bar</existing-element>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_in_list_mismatched_name(self):
        with self.assertRaises(exemel.MismatchedElementNameError):
            exemel.build({
                'mismatched-name': [
                    'foo',
                    self.existing_element,
                    'bar'
                ]
            })


class AttributeTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = exemel.build({
            '@alpha': 'a',
            '@bravo': 'b'
        })

        expected_xml = '<root alpha="a" bravo="b"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = exemel.build({
            'child': {
                '@alpha': 'a',
                '@bravo': 'b'
            }
        })

        expected_xml = """
            <root>
                <child alpha="a" bravo="b"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_int_value(self):
        actual_xml = exemel.build({
            '@test': 0
        })

        expected_xml = '<root test="0"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_boolean_value(self):
        actual_xml = exemel.build({
            '@test': True
        })

        expected_xml = '<root test="true"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_none_value(self):
        actual_xml = exemel.build({
            '@test': None
        })

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class NamespaceTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = exemel.build({
            '#ns': 'fake:ns'
        })

        expected_xml = '<root xmlns="fake:ns"/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = exemel.build({
            'child': {
                '#ns': 'fake:ns'
            }
        })

        expected_xml = """
            <root>
                <child xmlns="fake:ns"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_inherited(self):
        actual_xml = exemel.build({
            '#ns': 'fake:ns',
            'child': None
        })

        expected_xml = """
            <f:root xmlns:f="fake:ns">
                <f:child/>
            </f:root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_not_inherited(self):
        actual_xml = exemel.build({
            '#ns': 'fake:ns',
            'child': {
                '#ns': None
            }
        })

        expected_xml = """
            <f:root xmlns:f="fake:ns">
                <child/>
            </f:root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_list_items_different_namespaces(self):
        actual_xml = exemel.build({
            'myList': [
                {
                    '#ns': 'first:ns'
                },
                {
                    '#ns': 'second:ns'
                }
            ]
        })

        expected_xml = """
            <root>
                <myList xmlns="first:ns"/>
                <myList xmlns="second:ns"/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


class TextTestCase(xmlunittest.XmlTestCase):

    def test_on_root(self):
        actual_xml = exemel.build({
            '#text': 'foo'
        })

        expected_xml = '<root>foo</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_on_sub_element(self):
        actual_xml = exemel.build({
            'child': {
                '#text': 'foo'
            }
        })

        expected_xml = """
            <root>
                <child>foo</child>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_int_value(self):
        actual_xml = exemel.build({
            '#text': 0
        })

        expected_xml = '<root>0</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_float_value(self):
        actual_xml = exemel.build({
            '#text': 1.1
        })

        expected_xml = '<root>1.1</root>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_boolean_values(self):
        actual_xml = exemel.build({
            'child': [
                {
                    '#text': True
                },
                {
                    '#text': False
                }
            ]
        })

        expected_xml = """
            <root>
                <child>true</child>
                <child>false</child>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_none_value(self):
        actual_xml = exemel.build({
            '#text': None
        })

        expected_xml = '<root/>'

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)

    def test_text_and_sub_elements(self):
        dictionary = collections.OrderedDict()
        dictionary['alpha'] = None
        dictionary['#text'] = 'foo'
        dictionary['bravo'] = None

        actual_xml = exemel.build(dictionary)

        expected_xml = """
            <root>
                foo
                <alpha/>
                <bravo/>
            </root>
            """

        self.assertXmlEquivalentOutputs(actual_xml, expected_xml)


if __name__ == '__main__':
    unittest.main()

# exemel

Build XML documents easily and concisely using native Python data structures.

## Usage
```python
import exemel

xml = exemel.build({
    'name': 'John Doe',
    'address': {
        'street': '1 Main St.',
        'city': 'Exampletown',
        'zip': 12345
    },
    'phone': [
        '800-867-5309',
        {
            '#text': '555-555-5555',
            '@type': 'mobile'
        }
    ],
    'favorite': True
}, root='contact')
```

The return value would be an XML string equivalent to:
```xml
<contact>
    <name>John Doe</name>
    <address>
        <street>1 Main St.</street>
        <city>Exampletown</city>
        <zip>12345</zip>
    </address>
    <phone>800-867-5309</phone>
    <phone type="mobile">555-555-5555</phone>
    <favorite>true</favorite>
</contact>
```

The ``build`` function accepts a single positional argument: the dictionary-like object to convert into the root element. It also accepts two keyword arguments. The first, ``root``, can be used to supply a tag for the root element. If the argument is not provided, the root element will be named 'root'. The second, ``encoding``, determines the encoding of the resulting string. It defaults to a byte string if no argument is provided.

### Dictionaries
Any dictionary-like object (an instance of ``collections.abc.Mapping``) will be converted into an XML element. Each key in the dictionary is used to add sub-elements, attributes, or other properties to that element.

Any key that is not a decorator (see *Decorators*) will add one or more sub-elements.

```python
xml = exemel.build({
    'foo': 'bar'
})
```

```xml
<root>
    <foo>bar</foo>
</root>
```

**NOTE:** If using Python's ``dict`` type, which is unordered, the sub-elements in the resulting XML string will also be unordered. Order is often unimportant in XML aside from lists (see *Iterables* for ordering of list items). However, if ordering of sub-elements is important, you can use the ``collections.OrderedDict`` type.

```python
ordered_dict = collections.OrderedDict()
ordered_dict['first'] = 1
ordered_dict['second'] = 2
xml = exemel.build(ordered_dict)
```

```xml
<root>
    <first>1</first>
    <second>2</second>
</root>
```

### Iterables
Any non-string iterable (an instance of ``collections.abc.Iterable`` but not ``basestring``) will be converted into ordered sibling XML elements with the same tag. List items may be basic literals or dictionaries (they can be mixed).

```python
xml = exemel.build({
    'myList': [
        'simple',
        0,
        {'type': 'complex'}
    ]
})
```

```xml
<root>
    <myList>simple</myList>
    <myList>0</myList>
    <myList>
        <type>complex</type>
    </myList>
</root>
```

**NOTE:** Similarly to dictionaries, the order of the elements in the resulting XML string is dependent on the type of iterable. For example, an ordered iterable like a ``list`` will result ordered elements, but an unordered iterable like a ``set`` will result in unordered elements.

### Elements
Any ``lxml.etree.Element`` instance used as a value in a ``Mapping`` or an item in an ``Iterable`` will be added to the document as-is.

Within a ``Mapping``:

```python
my_element = etree.Element('myElement')
my_element.text = 'my-text'

xml = exemel.build({
    'myElement': my_element
})
```

```xml
<root>
    <myElement>my-text</myElement>
</root>
```

Within an ``Iterable``:

```python
my_element = etree.Element('myList')
my_element.text = 'my-text'

xml = exemel.build({
    'myList': [
        'foo',
        my_element,
        'bar'
    ]
})
```

```xml
<root>
    <myList>foo</myList>
    <myList>my-text</myList>
    <myList>bar</myList>
</root>
```

**NOTE:** If the name of the ``Element`` instance does not match the expected name, ``exemel.MismatchedElementNameError`` will be raised. E.g.:

```python
exemel.build({
    'oneName': etree.Element('anotherName')
})
```

would result in the following exception:

``exemel.MismatchedElementNameError: Element with name 'anotherName' was added where name 'oneName' was expected``

### Decorators
Decorators are special formats used in dictionary keys to add additional properties to an element.

#### Attribute Decorators
Any key prefixed with the ``@`` character will add an attribute to the element.

```python
xml = exemel.build({
    '@foo': 'bar'
})
```

```xml
<root foo="bar"/>
```

If the value is ``None``, the attribute will not be added. Otherwise, the value will be converted as described in *Converting Text*.

#### The Text Decorator
A key with the value ``#text`` can be used to add text to a complex element that couldn't be specified as just a string.

```python
xml = exemel.build({
    'example': {
        '@foo': 'bar',
        '#text': 'some text'
    }
})
```

```xml
<root>
    <example foo="bar">some text</example>
</root>
```

If the value is ``None``, no text will be added. Otherwise, the value will be converted as described in *Converting Text*.

#### The Namespace Decorator
Elements can be given a namespace by using the ``#ns`` decorator. Sub-elements will inherit the parent's namespace unless they specify their own namespace using the ``#ns`` decorator. Using ``None`` as the value sets the default namespace.

```python
xml = exemel.build({
    '#ns': 'foo',
    'one': None,
    'two': {
        '#ns': 'bar'
    },
    'three': {
        '#ns': None
    }
})
```

```xml
<f:root xmlns:f="foo">
    <f:one/>
    <b:two xmlns:b="bar"/>
    <three/>
</f:root>
```

Note that the namespace prefixes generated in the resulting XML string will be arbitrary. The prefixes used in the above example are simply for demonstration purposes.

### Creating Empty Elements
An element with no text, sub-elements, attributes, or namespace can be created by using ``None`` or an empty dictionary as the value.

```python
xml = exemel.build({
    'none': None,
    'empty': {}
})
```

```xml
<root>
    <none/>
    <empty/>
</root>
```

### Converting Text
For attributes and text nodes, values will be converted to text as follows:

* If the type is a boolean, values equal to ``True`` will become 'true', and values equal to ``False`` will become 'false'
* All other types will attempt to be converted using the ``str`` function


### Building an lxml.etree._Element instance
If you would like to use the [lxml.etree API](http://lxml.de/) directly, you can build an ``lxml.etree._Element`` instance instead of a string by using ``exemel.build_element()``. It's function signature is identical to that of ``exemel.build()``.

## Credit
This library was inspired by [xmlbuilder-js](https://github.com/oozcitak/xmlbuilder-js).

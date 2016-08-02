from ..namespaces import NAMESPACES
from ..exceptions import ElementDoesNotExist
import xml.etree.ElementTree as ET

class Element(object):
    def __init__(self, element):
        self._xml_element = element

    def __getitem__(self, key):
        """ Allows to use dictionary like notation to grab direct, (first) child of a given type """
        # TODO Is using dict notation the nicest way?
        # TODO that's a really sucky way to avoid circular dependencies
        from .text import P, Span
        # TODO Should we implement something like "spans" would return an array of Span?
        corresponding_class = next((c for c in [P, Span] if c.element == key), None)
        if corresponding_class is None:
            raise KeyError('Class not found for key {}'.format(key))
        elt = self._xml_element.find('{}:{}'.format(corresponding_class.namespace, corresponding_class.element), NAMESPACES)
        if elt is None:
            raise ElementDoesNotExist('Element not found')
        return corresponding_class(elt)

    @classmethod
    def create(cls, text=''):
        elt = ET.Element('{%s}%s' % (NAMESPACES[cls.namespace], cls.element))
        if text:
            elt.text = text
        return cls(elt)

    @property
    def text(self):
        return self._xml_element.text

    @text.setter
    def text(self, content):
        self._xml_element.text = content

    def insert(self, index, elt):
        # Might be inserting raw or pyopendoc element
        try:
            elt = elt._xml_element
        except AttributeError:
            pass
        self._xml_element.insert(index, elt)

    def append(self, elt):
        # Might be inserting raw or pyopendoc element
        try:
            elt = elt._xml_element
        except AttributeError:
            pass
        self._xml_element.append(elt)

class IndexableElement(Element):
    def _get_child_class(self):
        raise NotImplementedError

    def _get_child_selector(self):
        raise NotImplementedError

    def get_children(self):
        return [self._get_child_class()(elt) for elt in self._xml_element.findall(self._get_child_selector(), NAMESPACES)]

    def __getitem__(self, index):
        return self.get_children()[index]

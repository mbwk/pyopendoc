#!/usr/bin/env python3
from xml.etree import ElementTree

#
# Component Files
#

class SingleFileFactory():
    def load_file(self, filename, filebytes):
        if filename.endswith(".xml"):
            return SingleXMLFile(filename, filebytes)
        if imghdr.what(filename=None, h=filebytes):
            return SingleImageFile(filename, filebytes)
        return SingleUnknownFile(filename, filebytes)


class SingleFile(object):
    @property
    def filetype():
        raise NotImplementedError

    def to_bytes(self):
        raise NotImplementedError


class SingleXMLFile(SingleFile):
    def __init__(self, filename, filebytes):
        self.filename = filename
        self.root = ElementTree.fromstring(filebytes)

    @property
    def filetype(self):
        return "XML"

    def to_bytes(self):
        return bytes(ElementTree.tostring(self.root))

    def new_element(self, name="new", attributes={}):
        return ElementTree.Element(name, attributes)


class SingleImageFile(SingleFile):
    def __init__(self, filename, filebytes):
        self.filename = filename
        self.filebytes = filebytes

    @property
    def filetype(self):
        return "Image"

    def to_bytes(self):
        return self.filebytes


class SingleUnknownFile(SingleFile):
    def __init__(self, filename, filebytes):
        self.filename = filename
        self.filebytes = filebytes

    @property
    def filetype(self):
        return "Unknown"

    def to_bytes(self):
        return self.filebytes


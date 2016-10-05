#!/usr/bin/env python3
import zipfile
import tempfile
from io import (BytesIO)

from xml.etree import ElementTree as ET

from .singlefile import *
from .namespaces import NAMESPACES

#
# Open Document Files
#

class OpenDocument(object):


    def _fixup_xmlns(self, elem, maps=None):
        """
        At present, writes to file a duplicate set of namespaces. The elements/attributes within
        the file continue to use the old namespace references, but at least formulae seem to
        work on loading the file in Libreoffice
        """
        raise NotImplementedError
        if maps is None:
            maps = [{}]

        # Check for local overrides
        xmlns = {}
        xmlns_len = len(self.xmlns_str) + 1
        for key, value in elem.items():
            if key[:xmlns_len] == "{}:".format(self.xmlns_str):
                xmlns[value] = key[xmlns_len:]
        if xmlns:
            uri_map = maps[-1].copy()
            uri_map.update(xmlns)
        else:
            uri_map = maps[-1]

        #fixup this element
        fixup_element_prefixes(elem, uri_map, {})

        # recursively process sub-elements
        maps.append(uri_map)
        for elem in elem:
            self._fixup_xmlns(elem, maps)
        maps.pop()

    @property
    def CONTENT_FILE(self):
        return "content.xml"

    def get_content_file(self):
        return self.get_file(self.CONTENT_FILE)

    def __init__(self, filepath=None):
        self._open_files = {}
        self._document = None
        self._filename = ""
        self.__sff = SingleFileFactory()
        self.NAMESPACES = {}

        if filepath:
            self.open(filepath)

    def open(self, filepath):
        with open(filepath, "rb") as original_file:
            filelike = BytesIO(original_file.read())
        self._document = zipfile.ZipFile(filelike)
        self._filename = filepath

        self.NAMESPACES = NAMESPACES

    def close(self):
        self._document.close()
        self._document = None

    @property
    def _document(self):
        if self.__doc_file is not None:
            return self.__doc_file
        raise FileNotFoundError

    @_document.setter
    def _document(self, fileobj):
        self.__doc_file = fileobj

    def save(self, to=None):
        with zipfile.ZipFile(to if to else self._filename, mode="w") as savfile:
            for eafile in self._document.infolist():
                fname = eafile.filename
                if fname in self._open_files:
                    savfile.writestr(fname, self._open_files[fname].to_bytes())
                else:
                    file_data = self._document.read(fname)
                    savfile.writestr(eafile, file_data)

    def save_to_bytes(self):
        tmpfile = tempfile.TemporaryFile()
        with zipfile.ZipFile(tmpfile, mode="w") as memfile:
            for eafile in self._document.infolist():
                fname = eafile.filename
                if fname in self._open_files:
                    memfile.writestr(fname, self._open_files[fname].to_bytes())
                else:
                    file_data = self._document.read(fname)
                    memfile.writestr(eafile, file_data)
        tmpfile.seek(0)
        outbytes = tmpfile.read()
        tmpfile.close()
        return outbytes

    @property
    def _files_list(self):
        return self._document.namelist()

    def get_file(self, filepath):
        if filepath not in self._open_files:
            with self._document.open(filepath) as content:
                filebytes = content.read()
            single_file = self.__sff.load_file(filepath, filebytes)
            self._open_files[filepath] = single_file
        return self._open_files[filepath]

    def get_image_filename(self, imagename):
        raise NotImplementedError

    def replace_image(self, imagename, imagebytes):
        filename = self.get_image_filename(imagename)
        single_file = self.__sff.load_file(filename, imagebytes)
        self._open_files[filename] = single_file

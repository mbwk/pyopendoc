#!/usr/bin/env python3
import zipfile
import io

from .singlefile import *

NAMESPACES = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
}


#
# Open Document Files
#

class OpenDocument(object):

    @property
    def CONTENT_FILE(self):
        return "content.xml"

    def get_content_file(self):
        return self.get_file(self.CONTENT_FILE)

    def __init__(self, filepath=None):
        self._open_files = {}
        self._document = None
        self.__sff = SingleFileFactory()

        if filepath:
            self.open(filepath)
    
    def open(self, filepath):
        self._document = zipfile.ZipFile(filepath)

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
        with zipfile.ZipFile(to if to else self._document.filename, mode="w") as savfile:
            for eafile in self._document.infolist():
                fname = eafile.filename
                if fname in self._open_files:
                    savfile.writestr(fname, self._open_files[fname].to_bytes())
                else:
                    file_data = self._document.read(fname)
                    savfile.writestr(eafile, file_data)

    def save_to_bytesio(self):
        f = io.BytesIO()
        with zipfile.ZipFile(f, mode="w") as memfile:
            for eafile in self._document.infolist():
                fname = eafile.filename
                if fname in self._open_files:
                    memfile.writestr(fname, self._open_files[fname].to_bytes())
                else:
                    file_data = self._document.read(fname)
                    memfile.writestr(eafile, file_data)
        return f

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
        self._open_files[filename] = imagebytes


class OpenWriterDocument(OpenDocument):

    def set_variable(self, variable_name, value, target=None):
        target_file = target if target else self.CONTENT_FILE
        xml_file = self.get_file(target)
        if xml_file.filetype != "XML":
            raise TypeError
        
        for vs in xml_file.root.findall(".//text:variable-set", NAMESPACES):
            if varname == variable_name:
                vs.set("{%s}formula" % NAMESPACES["text"], "ooow:{}".format(value))
                vs.set("{%s}string-value" % NAMESPACES["text"], "{}".format(value))
                vs.text = value



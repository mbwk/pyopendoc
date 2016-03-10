#!/usr/bin/env python3


from .opendocument import OpenDocument
from .singlefile import *

class OpenWriterDocument(OpenDocument):

    def get_image_filename(self, image_name : str, target=None):
        target_file = target if target else self.CONTENT_FILE
        xml_file = self.get_file(target_file)
        if xml_file.filetype != "XML":
            raise TypeError("Not an XML file!")

        for df in xml_file.root.findall(".//draw:frame", self.NAMESPACES):
            imgname = df.get("{%s}name" % self.NAMESPACES["draw"])
            if imgname == image_name:
                child = df.find(".//draw:image", self.NAMESPACES)
                filename = child.get("{%s}href" % self.NAMESPACES["xlink"])
                if filename:
                    return filename
        raise KeyError("Could not find an image with that name")

    
    def set_variable(self, variable_name, value, target=None):
        target_file = target if target else self.CONTENT_FILE
        xml_file = self.get_file(target_file)
        if xml_file.filetype != "XML":
            raise TypeError("Not an XML file!")

        for vs in xml_file.root.findall(".//text:variable-set", self.NAMESPACES):
            varname = vs.get("{%s}name" % self.NAMESPACES["text"])
            if varname == variable_name:
                valtype = vs.get("{%s}value-type" % self.NAMESPACES["office"])
                if valtype == "float":
                    vs.set("{%s}formula" % self.NAMESPACES["text"], "ooow:{}".format(value))
                    vs.set("{%s}value" % self.NAMESPACES["text"], "{}".format(value))
                vs.text = value # needed for strings...


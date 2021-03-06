#!/usr/bin/env python3

from .elements import Span, Table
from .exceptions import ElementDoesNotExist
from .opendocument import OpenDocument
from .singlefile import *
import six


class OpenWriterDocument(OpenDocument):
    def __init__(self, filepath=None):
        super(OpenWriterDocument, self).__init__(filepath=filepath)
        self._tables = {}

    def get_image_filename(self, image_name, target=None):
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
                vs.text = str(value)  # needed for strings...

    def _get_table(self, table_name, target_file):
        xml_file = self.get_file(target_file)
        table = xml_file.root.find('.//table:table[@table:name="{}"]'.format(table_name), self.NAMESPACES)
        if table is None:
            raise ElementDoesNotExist('Table with name %s does not exist' % table_name)
        return Table(table)

    def write_to_table(self, table_name, column, row, value, refresh=False, target=None):
        """
        Use refresh to reload the table from the XML otherwise it uses a "cached" value
        """
        table = self._tables.get(table_name)
        if refresh or not table:
            target_file = target if target else self.CONTENT_FILE
            table = self._get_table(table_name, target_file)
            self._tables[table_name] = table

        # Grab the corresponding cell
        try:
            cell = table[row][column]
        except IndexError:
            raise ElementDoesNotExist('Corresponding cell does not exist')

        # Within, try to find span element, it's inside a p element
        # TODO Should we assume that we have a "p"?
        try:
            span = cell['p']['span']
        except ElementDoesNotExist:
            span = Span.create()
            cell['p'].append(span)

        span.text = value

    def write_to_frame(self, frame_name, x_value, y_value, value=None, target=None, unit="in"):
        """Writes to x, y coordinate of a specified frame.
        Defaults unit to inches.

        """
        target_file = target if target else self.CONTENT_FILE
        xml_file = self.get_file(target_file)
        if xml_file.filetype != "XML":
            raise TypeError("Not an XML file!")

        for df in xml_file.root.findall(".//draw:frame", self.NAMESPACES):
            frame = df.get("{%s}name" % self.NAMESPACES["draw"])
            if frame == frame_name:
                df.set("{%s}x" % self.NAMESPACES["svg"], "{}{}".format(x_value, unit))
                df.set("{%s}y" % self.NAMESPACES["svg"], "{}{}".format(y_value, unit))
                if value is not None:
                    if not isinstance(value, six.string_types):
                        raise ValueError('Value expected to be a string')
                    span = df.find(".//text:span", self.NAMESPACES)
                    span.text = value
                return

    def clone_table_row(self, table_name, row_index, new_row_index, target=None):
        target_file = target if target else self.CONTENT_FILE
        table = self._get_table(table_name, target_file)
        return table.clone_row(row_index, new_row_index)

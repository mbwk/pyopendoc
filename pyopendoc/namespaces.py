NAMESPACES = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "draw": "urn:oasis:names:tc:opendocument:xmlns:drawing:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0",
    "xlink": "http://www.w3.org/1999/xlink",
    "dc": "http://purl.org/dc/elements/1.1/",
    "meta": "urn:oasis:names:tc:opendocument:xmlns:meta:1.0",
    "number": "urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0",
    "svg": "urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0",
    "chart": "urn:oasis:names:tc:opendocument:xmlns:chart:1.0",
    "dr3d": "urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0",
    "math": "http://www.w3.org/1998/Math/MathML",
    "form": "urn:oasis:names:tc:opendocument:xmlns:form:1.0",
    "script": "urn:oasis:names:tc:opendocument:xmlns:script:1.0",
    "ooo": "http://openoffice.org/2004/office",
    "ooow": "http://openoffice.org/2004/writer",
    "oooc": "http://openoffice.org/2004/calc",
    "dom": "http://www.w3.org/2001/xml-events",
    "xforms": "http://www.w3.org/2002/xforms",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "rpt": "http://openoffice.org/2005/report",
    "of": "urn:oasis:names:tc:opendocument:xmlns:of:1.2",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "grddl": "http://www.w3.org/2003/g/data-view#",
    "officeooo": "http://openoffice.org/2009/office",
    "tableooo": "http://openoffice.org/2009/table",
    "drawooo": "http://openoffice.org/2010/draw",
    "calcext": "urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0",
    "loext": "urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0",
    "field": "urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0",
    "formx": "urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0",
    "css3t": "http://www.w3.org/TR/css3-text/"
}

import xml.etree.ElementTree as ET
for k, v in NAMESPACES.items():
    ET.register_namespace(k, v)

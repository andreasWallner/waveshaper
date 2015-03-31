import xml.etree.ElementTree as ET

class SVGSurface(object):
    def __init__(self):
        self._root = self._root_element()

    def _root_element(self):
        root = ET.Element('svg')
        return root

    def draw_line(self, c1, c2, color, linewidth):
        line = ET.SubElement(self._root, 'line')

        line.attrib['x1'] = str(c1.x)
        line.attrib['y1'] = str(c1.y)
        line.attrib['x2'] = str(c2.x)
        line.attrib['y2'] = str(c2.y)
        line.attrib['style'] = 'stroke:{};stroke-width:{};stroke-linecap:round'.format(
            color,
            linewidth)

        return line

    def draw_fill(self, vertices, color, linewidth):
        poly = ET.SubElement(self._root, 'polygon')

        points = ' '.join(['{},{}'.format(v.x,v.y) for v in vertices])
        poly.attrib['points'] = points

        poly.attrib['style'] = 'fill:{0};stroke:{0};stroke-width:{1}'.format(
            color,
            linewidth)

        return poly

    def draw_text(self, text, position):
        textEl = ET.SubElement(self._root, 'text')

        textEl.attrib['x'] = str(position.x)
        textEl.attrib['y'] = str(position.y)
        textEl.attrib['fill'] = 'black'

        textEl.text = text
    
    def write(self, file):
        et = ET.ElementTree(self._root)
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        et.write(
            file,
            encoding='utf8',
            xml_declaration=True,
            short_empty_elements=False,
            )

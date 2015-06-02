#! /usr/bin/env python

import sys
sys.path.append('/usr/share/inkscape/extensions')
import inkex
import os
import subprocess
import tempfile
import shutil


def create_temporary_copy(path):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, 'temp_file_name')
    shutil.copy2(path, temp_path)
    return temp_path


class PNGExport(inkex.Effect):
    def __init__(self):
        """init the effetc library and get options from gui"""
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--path", action="store", type="string", dest="path", default="~", help="")

    def effect(self):
        output_path = self.options.path
        curfile = self.args[-1]
        layer_ids = self.get_layer_ids(curfile)

        for layer_id in layer_ids:
            hide_layer_ids = set(layer_ids)
            hide_layer_ids.remove(layer_id)
            hide_layer_ids = list(hide_layer_ids)
            show_layer_ids = [layer_id]
            layer_dest_svg_path = curfile + layer_id + ".svg"
            layer_dest_png_path = output_path + layer_id + ".png"
            self.export_layers(curfile, layer_dest_svg_path, hide_layer_ids, show_layer_ids)
            self.exportPage(layer_dest_svg_path, layer_dest_png_path)

    def export_layers(self, src, dest, hide, show):
        """
        Export selected layers of SVG in the file `src` to the file `dest`.
        :arg  str    src:  path of the source SVG file.
        :arg  str   dest:  path to export SVG file.
        :arg  list  hide:  layers to hide. each element is a string.
        :arg  list  show:  layers to show. each element is a string.
        """
        for layer in self.document.xpath('//svg:g', namespaces=inkex.NSS):
            id = layer.attrib["id"]
            if id in hide:
                layer.attrib['style'] = 'display:none'
            elif id in show:
                layer.attrib['style'] = 'display:inline'

        self.document.write(dest)

    def get_layer_ids(self, src):
        layers = self.document.xpath('//svg:g', namespaces=inkex.NSS)
        layer_ids = []
        for layer in layers:
            layer_id = layer.attrib["id"]
            layer_ids.append(layer_id)

        return layer_ids

    def exportPage(self, svg_path, output_path):
        command = "inkscape -C -e \"%s\" %s" % (output_path, svg_path)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()


def _main():
    e = PNGExport()
    e.affect()
    exit()

if __name__ == "__main__":
    _main()

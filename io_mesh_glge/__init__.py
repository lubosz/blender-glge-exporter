# ##### BEGIN GPL LICENSE BLOCK #####
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>
# coding: utf-8

# To support reload properly, try to access a package var, if it's there, reload everything
if "bpy" in locals():
    import sys
    reload(sys.modules.get("io_mesh_glge.export_glge", sys))


import bpy
from bpy.props import *
from io_utils import ExportHelper


class ExportGLGE(bpy.types.Operator, ExportHelper):
    '''Export a GLGE Scene as XML with meshes, lights, camera, materials and objects.'''
    bl_idname = "export.xml"
    bl_label = "Export GLGE"
    
    filename_ext = ".xml"

    use_modifiers = BoolProperty(name="Apply Modifiers", description="Apply Modifiers to the exported mesh", default=True)
    use_normals = BoolProperty(name="Normals", description="Export Normals for smooth and hard shaded faces", default=True)
    use_uv_coords = BoolProperty(name="UVs", description="Export the active UV layer", default=True)
    compress_meshes = BoolProperty(name="Compress Meshes", description="Shorten the XML output of the mesh file", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)
        import io_mesh_glge.export_glge
        return io_mesh_glge.export_glge.save(self, context, **self.properties)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "use_modifiers")
        row.prop(self, "use_normals")
        row = layout.row()
        row.prop(self, "use_uv_coords")
        row = layout.row()
        row.prop(self, "compress_meshes")

def menu_func(self, context):
    self.layout.operator(ExportGLGE.bl_idname, text="GLGE (.xml)")


def register():
    bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()

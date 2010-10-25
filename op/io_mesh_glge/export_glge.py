# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# Copyright (C) 2010: Lubosz Sarnecki, lubosz@gmail.com

"""
This script exports GLGE XML files from Blender. It supports normals
and texture coordinates per face or per vertex.
Only one mesh can be exported at a time.
"""

import bpy, os

def save(operator, context, filepath="", use_modifiers=True, use_normals=True, use_uv_coords=True, use_colors=True):
    
    scene = context.scene
    obj = context.object
    meshname = obj.data.name

    if not obj:
        raise Exception("Error, Select 1 active object")

    file = open(filepath, 'w')

    if scene.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')

    if use_modifiers:
        mesh = obj.create_mesh(scene, True, 'PREVIEW')
    else:
        mesh = obj.data

    if not mesh:
        raise Exception("Error, could not get mesh data from active object")

    # mesh.transform(obj.matrix_world) # XXX

    faceUV = (len(mesh.uv_textures) > 0)
    vertexUV = (len(mesh.sticky) > 0)

    if (not faceUV) and (not vertexUV):
        use_uv_coords = False

    if not use_uv_coords:
        faceUV = vertexUV = False

    if faceUV:
        active_uv_layer = mesh.uv_textures.active
        if not active_uv_layer:
            use_uv_coords = False
            faceUV = None
        else:
            active_uv_layer = active_uv_layer.data

    file.write('<?xml version="1.0"?>\n')
    file.write('<!-- Created by Blender %s - www.blender.org, source file: %r -->\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)))
    file.write('<glge>\n')
    file.write("\t<mesh id=\"%s\">\n"  % (meshname))
    
    vertices = "\t\t<positions>"
    
    if use_normals:
        normals = "\t\t<normals>"
        
    if use_uv_coords:
        uv = mesh.uv_textures.active.data
        uvs = "\t\t<uv1>"
        
    indices = "\t\t<faces>\n\t\t\t"
    index = 0
    
    for i,f in enumerate(mesh.faces):
        for j,vertex in enumerate(f.vertices):
            vertices+= '\n\t\t\t%f,%f,%f,' % tuple(mesh.vertices[vertex].co)
            if use_normals:
                normals += '\n\t\t\t%f,%f,%f,' % tuple(f.normal) # no
        if use_uv_coords:
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv1)
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv2)
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv3)
            
            #uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv1)
            #uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv3)
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv4)
            
            
        indices += '%i,%i,%i,' % (index,index+1,index+2)
        if len(f.vertices) == 4:
            indices += '%i,%i,%i,' % (index,index+2,index+3)
        index+=len(f.vertices)

    file.write(vertices + "\n\t\t</positions>\n")
    if use_normals:
        file.write(normals + "\n\t\t</normals>\n")
    if use_uv_coords:
        file.write(uvs + "\n\t\t</uv1>\n")
    file.write(indices + "\n\t\t</faces>\n")

    file.write('\t</mesh>\n')
    file.write('</glge>\n')
    
    file.close()
    print("writing %r done" % filepath)

    if use_modifiers:
        bpy.data.meshes.remove(mesh)

    
    return {'FINISHED'}

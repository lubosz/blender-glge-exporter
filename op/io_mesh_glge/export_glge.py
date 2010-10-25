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

def save(operator, context, filepath="", use_modifiers=True, use_normals=True, use_uv_coords=True):
    
    scene = context.scene
    obj = context.object
    
    if not obj:
        raise Exception("Error, Select 1 active object")

    if scene.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
        
    file = open(filepath, 'w')
    file.write('<?xml version="1.0"?>\n')
    file.write('<!-- Created by Blender %s - www.blender.org, source file: %r -->\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)))
    file.write('<glge>\n')
    writeMesh(file, scene, obj,use_modifiers, use_normals, use_uv_coords)
    writeScene(file, scene)
    file.write('\n</glge>\n')
    file.close()
        
    print("writing %r done" % filepath)
    
    return {'FINISHED'}

def writeScene(file, scene):
    file.write('\t<scene id="%s" camera="#%s" ambient_color="#666" fog_type="FOG_NONE">' % (scene.name, scene.camera.name))

    for sceneObject in scene.objects:
        if sceneObject.type == "MESH":
            file.write('\n\t\t<object id="%s" mesh="#%s"' % (sceneObject.name, sceneObject.data.name))
            file.write(' scale_x="%f" scale_y="%f" scale_z="%f"' % tuple(sceneObject.scale))
            file.write(' rot_x="%f" rot_y="%f" rot_z="%f"' % tuple(sceneObject.rotation_euler))
            file.write(' loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(sceneObject.location))
            file.write(' material="#%s"' % sceneObject.material_slots.items()[0][0])
            file.write(' />')
            
        if sceneObject.type == "LAMP":
            file.write('\n\t\t<light id="%s"' % sceneObject.name)
            file.write(' loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(sceneObject.location))
            file.write(' attenuation_constant="0.5" type="L_POINT"')
            file.write(' />')
        
        if sceneObject.type == "CAMERA":
            file.write('\n\t\t<camera id="%s"' % sceneObject.name)
            file.write(' loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(sceneObject.location))
            file.write(' rot_order="ROT_XZY" xtype="C_PERSPECTIVE"')
            file.write(' rot_x="%f" rot_y="%f" rot_z="%f"' % tuple(sceneObject.rotation_euler))
            file.write(' />')

    file.write('\n\t</scene>')    

    
def writeMesh(file, scene, obj, use_modifiers, use_normals, use_uv_coords):
    meshname = obj.data.name
    
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
        lastFace = (i == len(mesh.faces)-1)
        for j,vertex in enumerate(f.vertices):
            lastVert = (j == len(f.vertices)-1 and lastFace)
            vertices+= '\n\t\t\t%f,%f,%f' % tuple(mesh.vertices[vertex].co)
            if not lastVert:
                vertices+="," 
            if use_normals:
                normals += '\n\t\t\t%f,%f,%f' % tuple(f.normal) # no
                if not lastVert:
                    normals+="," 
        if use_uv_coords:
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv1)
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv2)
            uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv3)
            
            #uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv1)
            #uvs += "\n\t\t\t%f,%f," % tuple(uv[i].uv3)
            uvs += "\n\t\t\t%f,%f" % tuple(uv[i].uv4)
            if not lastFace:
                uvs += ","
            
            
        indices += '%i,%i,%i' % (index,index+1,index+2)
        if len(f.vertices) == 4:
            indices += ',%i,%i,%i' % (index,index+2,index+3)
        if not lastFace:
            indices += ","
        index+=len(f.vertices)

    file.write(vertices + "\n\t\t</positions>\n")
    if use_normals:
        file.write(normals + "\n\t\t</normals>\n")
    if use_uv_coords:
        file.write(uvs + "\n\t\t</uv1>\n")
    file.write(indices + "\n\t\t</faces>\n")

    file.write('\t</mesh>\n')

    
    if use_modifiers:
        bpy.data.meshes.remove(mesh)
        
    print("writing of Mesh %r done" % meshname)


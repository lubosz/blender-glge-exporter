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
# coding: utf-8
# Author: Lubosz Sarnecki, lsarnecki@uni-koblenz.de

"""
This script exports GLGE XML files from Blender. It supports normals
and texture coordinates per face or per vertex.
Only one mesh can be exported at a time.
"""

import bpy, os

def save(operator, context, filepath="", use_modifiers=True, use_normals=True, use_uv_coords=True):
    
    scene = context.scene
    obj = context.object
    
    """
    if not obj:
        raise Exception("Error, Select 1 active object")

    if scene.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
    """
        
    file = open(filepath, 'w')
    file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    file.write('<!DOCTYPE glge SYSTEM "glge.dtd">\n')
    file.write('<!-- Created by Blender %s - www.blender.org, source file: %r -->\n' % (bpy.app.version_string, os.path.basename(bpy.data.filepath)))
    file.write('<glge>\n')
    writeMeshes(file)
    writeMaterials(file)
    writeScene(file, scene)
    file.write('\n</glge>\n')
    file.close()
        
    print("writing %r done" % filepath)
    
    return {'FINISHED'}

def writeScene(file, scene):
    if scene.world.mist_settings.use_mist:
        fog = 'FOG_QUADRATIC'
    else:
        fog = 'FOG_NONE'
    
    file.write('\n\t<scene id="%s" camera="#%s" ambient_color="%s" fog_type="%s">' 
               % (
                  scene.name,
                  scene.camera.name,
                  rgbColor(scene.world.ambient_color),
                  fog
                  )
               )
    #<group id="graph" animation="#spin">
    tagTab = "\n\t\t"
    elTab = "\n\t\t\t"
    for obj in scene.objects:
        if obj.type == "MESH":
            file.write(tagTab+'<object id="%s" mesh="#%s"' % (obj.name, obj.data.name))
            file.write(elTab+'loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(obj.location))
            file.write(elTab+'rot_x="%f" rot_y="%f" rot_z="%f"' % tuple(obj.rotation_euler))
            file.write(elTab+'scale_x="%f" scale_y="%f" scale_z="%f"' % tuple(obj.scale))
            file.write(elTab+'material="#%s"' % obj.material_slots.items()[0][0])
            if len(obj.material_slots[0].material.texture_slots.items()) > 0:
                if obj.material_slots[0].material.texture_slots[0].use_map_alpha:
                    file.write(elTab+'ztransparent="TRUE"')
            file.write(tagTab+'/>')
            #skeleton="#Armature" action="#Stand"
            
        if obj.type == "LAMP":
            file.write(tagTab+'<light id="%s"' % obj.name)
            file.write(elTab+'loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(obj.location))
            file.write(elTab+'rot_x="%f" rot_y="%f" rot_z="%f"' % tuple(obj.rotation_euler))
            file.write(elTab+'attenuation_constant="%f" attenuation_linear="%f" attenuation_quadratic="%f"' % (0.5,0.00000001,0.00001))
            #TODO: Alternative?
            #file.write(' color_r="%f" color_g="%f" color_b="%f"' % tuple(obj.data.color))
            file.write(elTab+'color="%s"' % rgbColor(obj.data.color))
            if obj.data.type == 'SUN':
                type = 'L_DIR'
            elif obj.data.type == 'SPOT':
                type = 'L_SPOT'
                shadowRes = 1024
                file.write(elTab+'buffer_width="%d" buffer_height="%d"' % (shadowRes,shadowRes))
                file.write(elTab+'shadow_bias="%f" spot_cos_cut_off="%f" spot_exponent="%f"' 
                           % 
                           #(5.0, 0.775, 50)
                           (2.5, 0.80, 40)
                )
                file.write(elTab+'cast_shadows="TRUE"')
              

            else:
                type = 'L_POINT'
            file.write(elTab+'type="%s"' % type)
            file.write(tagTab+' />')
        
        if obj.type == "CAMERA":
            file.write(tagTab+'<camera id="%s"' % obj.name)
            file.write(elTab+'loc_x="%f" loc_y="%f" loc_z="%f"' % tuple(obj.location))
            file.write(elTab+'rot_order="ROT_XZY" xtype="C_PERSPECTIVE"') #C_ORTHO
            file.write(elTab+'rot_x="%f" rot_y="%f" rot_z="%f"' % tuple(obj.rotation_euler))
            file.write(tagTab+'/>')

    file.write('\n\t</scene>')    

def writeMaterials(file):
    
    for material in bpy.data.materials:
        
        file.write('\n\t<material id="%s" color="%s" specular="%f" shininess="%f" emit="%f"'
                   % (
                      material.name,
                      rgbColor(material.diffuse_color),
                      material.specular_intensity,
                      material.specular_hardness,
                      material.emit
                      )
                   )
        #file.write(' reflectivity="%f"' % material.raytrace_mirror.reflect_factor)
        #file.write(' alpha="%f"' % '1.0')
        #file.write(' shadow = "TRUE"')
        file.write(' >')
        
        for texture_slot in material.texture_slots.items():
           
            texture = texture_slot[1].texture
            if texture.type == "IMAGE":
                
                if texture.use_normal_map:
                    target = 'M_NOR'
                else:
                    target = 'M_COLOR'
                    #M_HEIGHT M_MSKA M_SPECCOLOR
            
                file.write('\n\t\t<texture id="%s" src="%s" />' % (texture.name+"Tex", texture.image.filepath.replace("//","")))
                file.write('\n\t\t<material_layer texture="#%s" mapinput="%s" mapto="%s" />' % (texture.name+"Tex", 'UV1',target))
                if texture_slot[1].use_map_alpha:
                    file.write('\n\t\t<material_layer texture="#%s" mapinput="%s" mapto="%s" />' % (texture.name+"Tex", 'UV1','M_ALPHA'))
                #scale_y="10" alpha="0.5" blend_mode="BL_MUL"
                #mapinput MAP_ENV, MAP_OBJ, UV2
        file.write('\n\t</material>')
    
def writeMeshes(file):
    
    for mesh in bpy.data.meshes:
        writeMesh(file, mesh)

def rgbColor(color):
    return "rgb(%d,%d,%d)" % (color.r * 255, color.g * 255, color.b * 255)

def hexColor(color):
    #TODO: Too short strings
    hexColor = ""
    hexColor += "%x" % int(color.r * 255)
    hexColor += "%x" % int(color.g * 255)
    hexColor += "%x" % int(color.b * 255)
    return hexColor
    
#def writeMesh(file, scene, obj, use_modifiers, use_normals, use_uv_coords):
def writeMesh(file, mesh, use_normals=True, use_uv_coords=True):
    #meshname = obj.data.name
    
    """
    if use_modifiers:
        mesh = obj.create_mesh(scene, True, 'PREVIEW')
    else:
        mesh = obj.data
    """
    
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


    file.write("\t<mesh id=\"%s\">\n"  % (mesh.name))
    
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
                if f.use_smooth:
                    normals += '\n\t\t\t%f,%f,%f' % tuple(mesh.vertices[vertex].normal) # smooth?
                else:
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

    """
    if use_modifiers:
        bpy.data.meshes.remove(mesh)
    """
        
    print("writing of Mesh %r done" % mesh.name)


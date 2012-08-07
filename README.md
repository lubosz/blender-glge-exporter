Blender GLGE Exporter
=====================

A GLGE WebGL exporter for Blender 2.6

Installation
------------

Link or copy `io_mesh_glge` to `~/.blender/2.63/scripts/addons`

* mkdir ~/.blender/2.63/scripts/addons -p
* ln -s $PWD/io_mesh_glge/ ~/.blender/2.63/scripts/addons

Features
--------

* Blender 2.5 support
* Mesh export with UV coords and normals
* Scene export with objects, cameras and lights
* Modifier support
* Material color, texture, shading values and transparency
* 3 light types with colors and shadow maps in spot lights
* Normal and alpha maps
* Scene fog, ambient and background color
* Separates meshes, materials and scene in 3 files
* Nicely intended XML markup
* Optional short XML markup for mesh files

Running the example
-------------------

Link or copy the `GLGE` folder to `example`. You can clone [supereggbert's GLGE git repository](http://github.com/supereggbert/GLGE).
Put the `example` folder on your web server. GLGE does not work locally (only http://, no file://).
Of course you need a browser with WebGL support. You can check out a current Chromium or Firefox.

Hints
---------------

Textures have to be power of two. E.g. 16x16, 512x512, 1024x1024.

The support can vary in the specific browser implementation, but the spec
has only limited support for non-power-of-two-textures.

[More info at the Khronos wiki](http://www.khronos.org/webgl/wiki/WebGL_and_OpenGL_Differences)

You have to keep the same relative paths in Blender and GLGE currently. So put your .blend file in the meshes directory for example.

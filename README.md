Blender GLGE Exporter
=====================

A GLGE WebGL exporter for Blender 2.5

Installation
------------

Link or copy `io_mesh_glge` to `~/.blender/2.5X/scripts/addons`

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
Open `index.html` or put the `example` folder on your web server.
Of course you need a browser with WebGL support. You can check out a current Chromium or Firefox 4.

Hints
---------------

Textures have to be power of two. E.g. 16x16, 512x512, 1024x1024.

The support can vary in the specific browser implementation, but the spec
has only limited support for non-power-of-two-textures.

[More info at the Khronos wiki](http://www.khronos.org/webgl/wiki/WebGL_and_OpenGL_Differences)

You have to keep the same relative paths in Blender and GLGE currently. So put your .blend file in the meshes directory for example.
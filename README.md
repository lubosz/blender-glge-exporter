Blender GLGE Exporter
=====================

Installation
------------

Link or copy `io_mesh_glge` to `~/.blender/2.5X/scripts/op`

Running the example
-------------------

Link or copy the GLGE Folder to example and open `index.html` or put the example folder on your Webserver.

Exporting Hints
---------------

Textures have to be power of two. E.g. 16x16, 512x512, 1024x1024.

The support can vary in the specific browser implementation, but the spec
has only limited support for non-power-of-two-textures.
[More info at the Khronos wiki](http://www.khronos.org/webgl/wiki/WebGL_and_OpenGL_Differences)
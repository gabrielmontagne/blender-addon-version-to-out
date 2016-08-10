bl_info = {
    "name": "Output from VERSION.txt",
    "author": "gabriel montagné láscaris-comneno",
    "version": (0, 0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Sets render output from VERSION.txt file if found",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import bpy
from bpy.app.handlers import persistent

@persistent
def update_out_from_version(dummy):
    print("update out from version", dummy)

def register():
    bpy.app.handlers.render_pre.append(update_out_from_version)

def unregister():
    bpy.app.handlers.render_pre.remove(update_out_from_version)


if __name__ == "__main__":
    bpy.app.handlers.render_pre.clear() # HHA debug
    register()


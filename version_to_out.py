bl_info = {
    "name": "Output from VERSION.txt",
    "author": "gabriel montagné láscaris-comneno",
    "version": (0, 0, 1),
    "blender": (2, 75, 0),
    "description": "Sets render output from VERSION.txt file if found",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

from bpy.app.handlers import persistent
from os import path
import bpy

version_file = 'VERSION.txt'

@persistent
def update_out_from_version(dummy):
    base_dir = path.dirname(bpy.data.filepath)
    version_path = path.join(base_dir, version_file)
    if not path.isfile(path.join(base_dir, version_path)):
        return

    version = open(version_path, 'r').read().strip()

    print("VERSION", version)

def register():
    bpy.app.handlers.render_init.append(update_out_from_version)

def unregister():
    bpy.app.handlers.render_init.remove(update_out_from_version)

if __name__ == "__main__":
    ## HHA debug
    bpy.app.handlers.render_init.clear()

    register()

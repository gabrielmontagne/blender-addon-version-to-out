bl_info = {
    "name": "Output from VERSION.txt",
    "author": "gabriel montagné láscaris-comneno, gabriel@tibas.london",
    "version": (0, 3, 0),
    "blender": (2, 75, 0),
    "description": "Sets render output from VERSION.txt file if found",
    "category": "Render"
    }

from bpy.app.handlers import persistent
from os import path
import bpy

version_file = 'VERSION.txt'

@persistent
def update_out_from_version(scene):
    filepath = bpy.data.filepath
    base_dir = path.dirname(filepath)

    version_path = path.join(base_dir, version_file)
    if not path.isfile(path.join(base_dir, version_path)):
        return

    base = path.basename(filepath)
    name, ext = path.splitext(base)

    basename = path.basename(scene.render.filepath)
    version = open(version_path, 'r').read().strip()
    scene.render.filepath = '//target/{}/{}/{}'.format(version, name, basename)

def register():
    bpy.app.handlers.render_init.append(update_out_from_version)

def unregister():
    bpy.app.handlers.render_init.remove(update_out_from_version)

if __name__ == "__main__":
    register()

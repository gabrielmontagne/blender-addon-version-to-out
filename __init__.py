bl_info = {
    "name": "Output from VERSION.txt",
    "author": "gabriel montagné láscaris-comneno, gabriel@tibas.london",
    "version": (3, 0, 0),
    "blender": (2, 80, 0),
    "description": "Sets render output from VERSION.txt file if found",
    "category": "Render"
    }

from bpy import ops
from bpy.app.handlers import persistent
from bpy.path import abspath, basename
from bpy.props import BoolProperty
from bpy.types import Panel, Scene, Operator
from os import path, makedirs
from shlex import split
from subprocess import check_output
import bpy

version_map = {}
version_file = 'VERSION.txt'

def to_versioned_filepath(scene, basename=None, use_markers=True):
    global version_map

    filepath = bpy.data.filepath
    base_dir = path.dirname(filepath)
    version_path = path.join(base_dir, version_file)

    base = path.basename(filepath)
    name, ext = path.splitext(base)

    if not scene:
        scene = bpy.context.scene

    if not basename:
        basename = path.basename(scene.render.filepath)

    if not path.isfile(path.join(base_dir, version_path)):
        return scene.render.filepath

    version = version_map.get(version_path)
    if not version:

        version = open(version_path, 'r').read().strip()
        if scene.add_git_branch:
            version = '{}/{}'.format(check_output(split('git branch --show-current')).decode('utf8').strip(), version)

        version_map[version_path] = version

    if use_markers and scene.subfolder_per_mark:
        markers = [m for m in sorted(list(scene.timeline_markers), key=lambda m: m.frame) if m.frame <= scene.frame_current]
        if len(markers):
            last_marker = markers[-1]
            filepath = '//target/{}/{}/{}/{}/{}'.format(version, name, scene.name, last_marker.name, basename)
        else:
            filepath = '//target/{}/{}/{}/{}'.format(version, name, scene.name, basename)
    else:
        filepath = '//target/{}/{}/{}/{}'.format(version, name, scene.name, basename)

    return filepath

class RENDER_SOUND_OT_versioned_mixdown(Operator):
    bl_idname = 'sound.versioned_mixdown'
    bl_label = 'Mixdown audio and sound to versioned file'

    def execute(self, context):
        filepath = to_versioned_filepath(context.scene, 'audio.flac', False)
        folder, name = path.split(abspath(filepath))
        makedirs(folder, exist_ok=True)
        print(f'Mixing down to {name} on {folder}')
        bpy.ops.sound.mixdown(filepath=filepath, codec='FLAC', relative_path=True)
        return {'FINISHED'}

@persistent
def update_out_from_version(_):
    scene = bpy.context.scene
    scene.render.filepath = to_versioned_filepath(scene)

@persistent
def flush_version_cache():
    global version_map
    version_map = {}
    update_out_from_version()

class VERSION_TO_OUT_PT_config(Panel):
    bl_label = 'Version to out'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'output'

    def draw(self, context):
        layout = self.layout
        rd = context.scene.render
        row = layout.row()
        row.label(text='Create subfolders per mark')
        row.prop(context.scene, "subfolder_per_mark", text="")

        row = layout.row()
        row.label(text='Add git branch')
        row.prop(context.scene, "add_git_branch", text="")

        row = layout.row()
        row.prop(rd, "filepath", text="")

def register():
    Scene.subfolder_per_mark = BoolProperty(
        name='Nest in subfolders per mark',
        default=False)

    Scene.add_git_branch = BoolProperty(
        name='Add git branch to version',
        default=True)

    bpy.utils.register_class(VERSION_TO_OUT_PT_config)
    bpy.utils.register_class(RENDER_SOUND_OT_versioned_mixdown)

    bpy.app.handlers.save_pre.append(flush_version_cache)
    bpy.app.handlers.frame_change_pre.append(update_out_from_version)
    bpy.app.handlers.load_post.append(update_out_from_version)

def unregister():
    del Scene.subfolder_per_mark
    del Scene.add_git_branch
    bpy.app.handlers.frame_change_pre.remove(update_out_from_version)
    bpy.app.handlers.load_post.remove(update_out_from_version)
    bpy.app.handlers.save_pre.remove(flush_version_cache)

    bpy.utils.unregister_class(RENDER_SOUND_OT_versioned_mixdown)
    bpy.utils.unregister_class(VERSION_TO_OUT_PT_config)

if __name__ == "__main__":
    register()

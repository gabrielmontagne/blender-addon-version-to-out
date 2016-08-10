blender addon for rendering to versioned output folders
=======================================================
version: 0.1.0

When you hit 'Render', this addon will search for a ``VERSION.txt`` file next to the blend file.
If found, it will set the output to be `target/{version}/frame-`.

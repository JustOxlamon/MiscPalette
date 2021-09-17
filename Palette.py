#  ***** GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#  ***** GPL LICENSE BLOCK *****

import bpy
import json
import os
from bpy.props import (StringProperty,CollectionProperty)

bl_info = {
	'name': 'Misc Palette',
	'description': 'Palette toolbar in 3dView',
	'author': 'oxlamon',
	'license': 'GPL',
	'version': (1, 0, 0),
	'blender': (2, 93, 0),
	'location': 'View3D > Tools > Misc',
	'category': '3D View'
}

class MY_PP_CreateEmptyPalette(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "object.create_palette"
	bl_label = "Create palette"
	bl_options = {'REGISTER', 'INTERNAL'}

	def execute(self, context):
		pal = bpy.data.palettes.get("RTPalette")
		if pal is None:
			pal = bpy.data.palettes.new("RTPalette")
		else:
			pal.colors.clear()
		bpy.context.tool_settings.image_paint.palette=bpy.data.palettes.get("RTPalette")
		return {'FINISHED'}

	def invoke(self, context, event):
		return context.window_manager.invoke_confirm(self, event)

class MY_PP_ImportPalette(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "object.import_palette"
	bl_label = "Import palette"

	filename_ext = ".json"
	filter_glob: StringProperty(default="*.json", options={'HIDDEN'})    


	#this can be look into the one of the export or import python file.
	#need to set a path so so we can get the file name and path
	filepath: StringProperty(name="File Path", description="Filepath used for importing json palette files", maxlen= 1024, default= "")
	files: CollectionProperty(
		name="File Path",
		type=bpy.types.OperatorFileListElement)

	def execute(self, context):
		print(self.filepath)
		pal = bpy.data.palettes.get("RTPalette")
		if pal is None:
			pal = bpy.data.palettes.new("RTPalette")
		else:
			pal.colors.clear()
		bpy.context.tool_settings.image_paint.palette=bpy.data.palettes.get("RTPalette")

		with open(self.filepath) as f:
			dataDict = json.load( f )
			for item in dataDict:
				print(item)
				c = pal.colors.new()
				c.color = ( item["color"][0], item["color"][1], item["color"][2] )
				c.weight = item["weight"]
				c.strength = item["value"]

		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}

class MY_PP_ExportPalette(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "object.export_palette"
	bl_label = "Export palette"

	filename_ext = ".json"
	filter_glob: StringProperty(default="*.json", options={'HIDDEN'})    


	#this can be look into the one of the export or import python file.
	#need to set a path so so we can get the file name and path
	filepath: StringProperty(name="File Path", description="Filepath used for exporting json palette files", maxlen= 1024, default= "")
	files: CollectionProperty(
		name="File Path",
		type=bpy.types.OperatorFileListElement)

	def execute(self, context):
		pal = bpy.data.palettes.get("RTPalette")
		colordict = []
		for c in pal.colors:
			colordict.append({ "color": [ c.color[0], c.color[1], c.color[2] ], "value": c.strength, "weight": c.weight })
		fileData = json.dumps(colordict, indent=1, ensure_ascii=True)

		with open(self.filepath, 'w') as f:
			f.write(fileData)		
		return {'FINISHED'}
	
	def invoke(self, context, event):
		wm = context.window_manager
		wm.fileselect_add(self)
		return {'RUNNING_MODAL'}

class PalettePanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Palette"
	bl_idname = "OBJECT_PT_PalettePanel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'

	def draw(self, context):
		layout = self.layout
		pal = bpy.data.palettes.get("RTPalette")
		row = layout.row()
		row.operator(MY_PP_CreateEmptyPalette.bl_idname)
		row.operator(MY_PP_ImportPalette.bl_idname)
		if not(pal is None):
			row.operator(MY_PP_ExportPalette.bl_idname)
		layout.template_palette(context.tool_settings.image_paint, 'palette', color=False)

def register():
	bpy.utils.register_class(PalettePanel)
	bpy.utils.register_class(MY_PP_CreateEmptyPalette)
	bpy.utils.register_class(MY_PP_ExportPalette)
	bpy.utils.register_class(MY_PP_ImportPalette)

def unregister():
	bpy.utils.unregister_class(PalettePanel)
	bpy.utils.unregister_class(MY_PP_CreateEmptyPalette)
	bpy.utils.unregister_class(MY_PP_ExportPalette)
	bpy.utils.unregister_class(MY_PP_ImportPalette)


if __name__ == "__main__":
    register()

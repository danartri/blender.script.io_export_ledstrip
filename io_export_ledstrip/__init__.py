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
#
#  ***** GPL LICENSE BLOCK *****

bl_info = {
	"name": "Export LED strip (.xml)",
	"author": "Martin Froehlich (maybites.ch) & Aurelio Lucchesi (0rel.com)",
	"version": (0, 0, 1),
	"blender": (2, 7, 0),
	"location": "File > Export > ledstrip (.xml)",
	"description": "The script exports Blender curves to custom XML.",
	"warning": "Quick and dirty hack, no success guaranteed.",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"
}

# Ensure that we reload our dependencies if we ourselves are reloaded by Blender
if "bpy" in locals():
	import imp;
	if "exporter" in locals():
		imp.reload(exporter);


import bpy
from .exporter import Exporter

from bpy.props import BoolProperty
#from bpy.props import EnumProperty
#from bpy.props import StringProperty
from bpy.props import IntProperty


class ExportLedstrip(bpy.types.Operator):
	"""Export selection to ledstrip"""
	
	bl_idname = "ledstrip.xml"
	bl_label = "ledstrip XML exporter"
	bl_options = {'PRESET'}
	filename_ext = ".xml"
	
	filepath = StringProperty( subtype='FILE_PATH' )
	
	
	# Export options
	
	Verbose = BoolProperty(
		name="Verbose",
		description="Run the exporter in debug mode. Check the console for output",
		default=False )
	
	#CoordinateSystem = EnumProperty(
	#	name="Coordinate System",
	#	description="Use the selected coordinate system for export",
	#	items=(('LEFT_HANDED', "Left-Handed", "Use a Y up, Z forward system or a Z up, -Y forward system"),
	#		('RIGHT_HANDED', "Right-Handed", "Use a Y up, -Z forward system or a Z up, Y forward system")),
	#	default='LEFT_HANDED' )
	
	Resolution = IntProperty(
		name = 'Resolution',
		description = 'Resolution of mesh',
		default = 4,
		min = 1, max = 64 )
	
	
	def execute(self, context):
		
		self.filepath = bpy.path.ensure_ext(self.filepath, '.xml')
	
		from . import exporter
		Exporter = exporter.Exporter(self, context)
		Exporter.execute()
		return {'FINISHED'}
	
	def invoke(self, context, event):
		
		# Check currently selected objects
		curve_ok = False
		for obj in bpy.context.selected_objects:
			if obj.type == 'CURVE':
				curve_ok = True
				break
		if len(bpy.context.selected_objects) == 0 or not curve_ok:
			raise NameError( 'Please select at least one curve object!' )
			return {'CANCELLED '}
		
		if not self.filepath:
			self.filepath = bpy.path.ensure_ext( bpy.data.filepath, ".xml" )
		context.window_manager.fileselect_add( self )
		return {'RUNNING_MODAL'}







def menu_func(self, context):
	self.layout.operator(ExportLedstrip.bl_idname, text="ledstrip (.xml)");

def register():
	bpy.utils.register_module(__name__);
	bpy.types.INFO_MT_file_export.append(menu_func);

def unregister():
	bpy.utils.unregister_module(__name__);
	bpy.types.INFO_MT_file_export.remove(menu_func);

if __name__ == "__main__":
	register()

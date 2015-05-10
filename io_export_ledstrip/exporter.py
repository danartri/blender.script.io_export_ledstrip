import bpy


class Exporter:
	
	def __init__(self, Config, context):
		
		self.Config = Config
		self.context = context
		
		self.log( "ledstrip exporter" )
		self.log( "begin verbose logging..." )
	
	
	def execute(self):
		
		ledstripXML = ''
		selections = bpy.context.selected_objects
		scn = bpy.context.scene
		active_obj = scn.objects.active
		
		# ensure Blender is currently in OBJECT mode to allow data access.
		bpy.ops.object.mode_set(mode = 'OBJECT')
		
		# for all curves in selection
		for obj in selections:
			for group in obj.users_group:
				for obj in group.objects:
					if( obj.type == 'CURVE' ):
						
						self.log( 'converting curve %s' % obj.name )
						self.log( 'location: %s' % obj.location )
						
						ledstripXML += '\t<segment name="{}">\n'.format( obj.name )
						
						#for spline in obj.data.splines:
						#	self.log( 'number of bezier points: ', len( spline.bezier_points ) )
						#	for point in spline.bezier_points:
						#		self.log( 'coord: ', point.co )
						#		self.log( 'left handle: ', point.handle_left )
						#		self.log( 'right handle: ', point.handle_right )
						#		
						#		frmt = '\t<coord x="{:.2f}" y="{:.2f}" z="{:.2f}"></coord>\n'
						#		ledstripXML += frmt.format( point.co.x, point.co.y, point.co.z )
						
						
						# create mesh out of curve
						bpy.ops.object.select_all( action='DESELECT' ) 
						scn.objects.active = obj
						obj.select = True
						
						def0 = obj.data.resolution_u
						def1 = obj.data.fill_mode
						def2 = obj.data.bevel_resolution
						def3 = obj.data.bevel_depth
						
						obj.data.fill_mode = 'FULL'
						obj.data.resolution_u = self.Config.Resolution
						obj.data.bevel_resolution = 1 #resolution
						obj.data.bevel_depth = 0.0 #thickness
						bpy.ops.object.convert( target='MESH', keep_original=True )
						
						bpy.ops.group.objects_remove_all()
						
						obj.data.resolution_u = def0
						obj.data.fill_mode = def1           #reverting
						obj.data.bevel_resolution = def2
						obj.data.bevel_depth = def3
						
						
						# dump(obj.data)
						newObj = scn.objects.active
						mesh = newObj.data
						self.log( 'number of vertices=%d' % len(mesh.vertices) )
						for vert in mesh.vertices:
							self.log( 'v %f %f %f' % (vert.co.x, vert.co.y, vert.co.z) )
							frmt = '\t\t<coord x="{:.2f}" y="{:.2f}" z="{:.2f}"></coord>\n'
							ledstripXML += frmt.format( vert.co.x, vert.co.y, vert.co.z )
						
						#self.log( 'number of faces=%d' % len(mesh.polygons) )
						#for face in mesh.polygons:
						#	self.log('face')
						#	for vert in face.vertices:
						#		self.log(vert)
						
						
						# delete temporary mesh object
						bpy.ops.object.delete( use_global=False )
						
						ledstripXML += '\t</segment>\n'
		
		
		# restore previous selection
		bpy.ops.object.select_all(action='DESELECT')
		for obj in selections:
			obj.select = True
		scn.objects.active = active_obj
		
		# open the file and export XML
		with open( self.Config.filepath, 'w' ) as f: # self.filepath, 'w' ) as f:
			f.write( '<ledstrip>\n' )
			f.write( ledstripXML )
			f.write( '</ledstrip>\n' )
		
		self.log("ledstrip exported (%s)" % self.Config.filepath, MessageVerbose=True )
		
		return True
	
	
	def log( self, String, MessageVerbose=False ):
		if self.Config.Verbose is True or MessageVerbose == True:
			print( String )

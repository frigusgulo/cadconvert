import geopandas as gpd 
import os
import pyproj
from shapely.geometry import Point, LineString,Polygon
import pdb
class convert:
	def __init__(self,
		infile: str,
		qcadpath:str,
		crs = "EPSG:32611"):

		self.crs = crs
		self.infile = infile
		self.qcadpath = qcadpath
		self.file = None
		
		self.filedir = os.path.join(os.path.splitext(self.infile)[0],"Processed_From_Here")
		self.filedir_shape = os.path.join(self.filedir,"shapefiles")
		self.filedir_cad = os.path.join(self.filedir,"cadfiles")

		try:
			os.makedirs(self.filedir)
			os.makedirs(self.filedir_shape)
			os.makedirs(self.filedir_cad)
		except Exception as e:
			pass
			#print(f"Directory Construction Failed For {self.filedir}:\n {e}\n")

    	
		#pdb.set_trace()
		self.reformat()

	def reformat(self):
		output = str(os.path.join(self.filedir_cad,os.path.basename(os.path.splitext(self.infile)[0])+".dxf"))
		if not os.path.isfile(output):
			print(f"\n{self.infile} --> {output}\n")
			os.system(self.qcadpath+ " -r=R27 " + "-outfile="+output +" "+str(self.infile))
		self.file=output

	def load(self):
		mine = gpd.read_file(self.file)
		self.mine = gpd.GeoDataFrame(mine)
		self.mine.crs = self.crs
		self.crs_utm = pyproj.CRS(self.crs)
		self.mine.to_crs(self.crs_utm)

	def check_exception(self):
		if converter.mine["geometry"][0].bounds[0] < 100000:
			print(f"Converting Geoseries\n")
			self.mine["geometry"] = self.mine.translate(515960-9000,4084266-9000)


	def to_file(self):

		try:
			self.dfpoints = self.mine[self.mine["geometry"].apply(lambda x: isinstance(x,Point)) ]
			pointpath = os.path.basename(os.path.splitext(self.infile)[0])+"_points.shp"
			pointpath = os.path.join(self.filedir_shape,pointpath)
			if not os.path.isfile(pointpath):
				self.dfpoints.to_file(pointpath,driver="ESRI Shapefile")
		except Exception as e:
			print(f"Point File Construction Failed For {self.infile}:\n {e}\n")


		try:
			self.dflines =  self.mine[self.mine["geometry"].apply(lambda x: isinstance(x,LineString)) ]
			linepath = os.path.basename(os.path.splitext(self.infile)[0])+"_lines.shp"
			linepath = os.path.join(self.filedir_shape,linepath)
			if not os.path.isfile(linepath):
				self.dflines.to_file(linepath,driver="ESRI Shapefile")
		except Exception as e:
			print(f"Line File Construction Failed For {self.infile}:\n {e}\n")


		try:
			self.dfpolygons = self.mine[self.mine["geometry"].apply(lambda x: isinstance(x,Polygon)) ]
			polygonpath = os.path.basename(os.path.splitext(self.infile)[0])+"_polys.shp"
			polygonpath = os.path.join(self.filedir_shape,polygonpath)
			if not os.path.isfile(polygonpath):
				self.dfpolygons.to_file(polygonpath,driver="ESRI Shapefile")

		except Exception as e:
			print(f"Polygon File Construction Failed For {self.infile}:\n {e}\n")

	def run(self):
		try:
			self.load()
			self.check_exception()
			self.to_file()
		except Exception as e:
			print(f"Run Failed For {self.infile}:\n {e}\n")


import geopandas as gpd 
import os
import pyproj
from shapely.geometry import Point, LineString,Polygon

class convert:
	def __init__(self,
		infile: str,
		outfile: str,
		qcadpath:str,
		crs = "EPSG:32610"):
	self.crs = crs
	self.infile = infile
	self.outfile = outfile
	self.qcadpath = qcadpath
	self.file = None



	def reformat(self):
		output = os.path.join(os.path.splitext(self.infile)[0],".dxf")
		os.system(qcadpath+ "-r=R27 " + "-outfile="+output +" "+self.infile)
		self.file=output

	def load(self):
		mine = gpd.read_file(self.file)
		mine = gpd.GeoDataFrame(mine)
		mine.crs = self.crs
		crs_utm = pyproj.CRS(self.crs)
		mine.to_crs(crs_utm)
		self.dfpoints = mine[mine["geometry"].apply(lambda x: isinstance(x,Point)) ]
		self.dflines =  mine[mine["geometry"].apply(lambda x: isinstance(x,LineString)) ]
		self.dfpolygons = mine[mine["geometry"].apply(lambda x: isinstance(x,Polygon)) ]

	def write(self):
		pointpath = os.path.join(self.outfile,"_points.shp")
		linepath = os.path.join(self.outfile,"_lines.shp")
		polygonpath = os.path.join(self.outfile,"_polys.shp")

		self.dfpoints.to_file(pointpath,driver="ESRI Shapefile")
		self.dflines.to_file(linepath,driver="ESRI Shapefile")
		self.polygonpath.to_file(polygonpath,driver="ESRI Shapefile")

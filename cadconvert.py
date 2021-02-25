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
		self.reformat()



	def reformat(self):
		output = os.path.splitext(self.infile)[0]+".dxf"
		os.system(self.qcadpath+ "-r=R27 " + "-outfile="+output +" "+self.infile)
		self.file=output

	def load(self):
		mine = gpd.read_file(self.file)
		mine = gpd.GeoDataFrame(mine)
		mine.crs = self.crs
		crs_utm = pyproj.CRS(self.crs)
		mine.to_crs(crs_utm)
		try:
			self.dfpoints = mine[mine["geometry"].apply(lambda x: isinstance(x,Point)) ]
			pointpath = self.outfile+"_points.shp"
			self.dfpoints.to_file(pointpath,driver="ESRI Shapefile")
		except:
			print(f"\n Points Not Fond\n")
		try:
			self.dflines =  mine[mine["geometry"].apply(lambda x: isinstance(x,LineString)) ]
			linepath = self.outfile+"_lines.shp"
			self.dflines.to_file(linepath,driver="ESRI Shapefile")
		except:
			print(f"\n Lines Not Fond\n")
		try:
			self.dfpolygons = mine[mine["geometry"].apply(lambda x: isinstance(x,Polygon)) ]
			polygonpath = self.outfile+"_polys.shp"
			self.dfpolygons.to_file(polygonpath,driver="ESRI Shapefile")

		except:
			print(f"\n Polygons Not Fond\n")


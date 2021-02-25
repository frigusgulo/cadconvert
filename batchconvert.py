import os
from cadconvert import convert 
from glob import glob

qcadpath = "/home/fdunbar/Applications/qcad-3.25.2-pro-linux-x86_64/dwg2dwg "
dwgfiles = glob("/home/fdunbar/bullfrog/GEOPHY/DRAWINGS/*.DWG")
strips = [os.path.splitext(file)[0] for file in dwgfiles]
converters = [convert(dwgfiles,strips,qcadpath) for (dwgfiles,strips) in zip(dwgfiles,strips)]
[converter.load() for converter in converters]

import os
from cadconvert import convert 
from glob import glob
import shutil
from pathlib import Path
qcadpath = "/home/dunbar/Apps/qcad-3.26.2-pro-linux-x86_64/dwg2dwg"

root_dir = "/home/dunbar/Hillary/BarrickData"
for root,dirs,files in os.walk(root_dir):
	for directory in dirs:
		newdir = directory.replace(" ","").replace("\t","")
		if newdir is not directory:
			shutil.move(os.path.join(root,directory),os.path.join(root,newdir))

print(f"\n Cleaning Files \n")
for root,dirs,files in os.walk(root_dir):
	for file in files:
		newfile = file.replace(" ","").replace("\t","")
		if newfile is not file:
			os.rename(os.path.join(root,file),os.path.join(root,newfile))
			
print("Gathering Cad Files")

dwgfiles = [path for path in Path(root_dir).rglob("*.DWG")] 
dwgfiles.extend([path for path in Path(root_dir).rglob("*.dwg")] )
print("Converting Files")
converters = [convert(dwgfiles,qcadpath) for dwgfiles in dwgfiles]
print(len(converters))
[converter.run() for converter in converters]

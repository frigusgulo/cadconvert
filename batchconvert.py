import os
from cadconvert import convert 
from glob import glob
import shutil
from pathlib import Path
qcadpath = "/home/dunbar/Apps/qcad-3.26.2-pro-linux-x86_64/dwg2dwg"

root_dir = "/home/dunbar/Hillary/BarrickData"
for root,dirs,files in os.walk(root_dir):
	for directory in dirs:
		newdir = directory.replace(" ","").replace("\t","").replace("\'","").replace("-","_").replace(",","").replace("&","_and_").replace("(","").replace(")","")
		if newdir is not directory:
			shutil.move(os.path.join(root,directory),os.path.join(root,newdir))

print(f"\n Cleaning Files \n")
for root,dirs,files in os.walk(root_dir):
	for file in files:
		newfile = file.replace(" ","").replace("\t","").replace("\'","").replace("-","_").replace(",","").replace("&","_and_").replace("(","").replace(")","")
		if newfile is not file:
			os.rename(os.path.join(root,file),os.path.join(root,newfile))

print("\nConverting WK1 Files\n")
spreadfiles = [path for path in Path(root_dir).rglob(".WK?")]
spreadfiles.extend([path for path in Path(root_dir).rglob(".xl??")])

spreads = [convert(path,cadfile=False) for path in spreadfiles]


dwgfiles = [path for path in Path(root_dir).rglob("*.DWG")] 
dwgfiles.extend([path for path in Path(root_dir).rglob("*.dwg")] )
print("\nConverting Files\n")
converters = [convert(dwgfile,qcadpath) for dwgfile in dwgfiles]
total = len(converters)
print(total)
count = 0
for converter in converters:
	try:
		converter.run()
		count += 1
	except Exception as e:
		print(e)
print(f"Successfull Processes: {(count/total)*100}%")


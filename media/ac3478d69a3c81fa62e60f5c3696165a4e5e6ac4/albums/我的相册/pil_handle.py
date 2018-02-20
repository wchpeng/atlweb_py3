#! /usr/bin/python3

from PIL import Image
import os

current_folder = os.getcwd()
print(current_folder)

current_files = os.listdir(current_folder)
print(current_files)

for f in current_files:
	if not f.endswith("py"):
		im = Image.open(f)
		w, h = im.size

		if w >= h:
			w_offset = int((w-h)*0.5)
			box = (w_offset, 0, w_offset+h, h)
			region = im.crop(box)
			name_tuple = os.path.splitext(f)
			region.save(name_tuple[0] +".copy" + name_tuple[1])
		else:
			h_offset = int((h-w)*0.5)
			box = (0, h_offset, w, h_offset+w)
			region = im.crop(box)
			name_tuple = os.path.splitext(f)
			region.save(name_tuple[0] +".copy" + name_tuple[1])
		os.remove(f)
		os.rename(name_tuple[0] +".copy" + name_tuple[1], f)

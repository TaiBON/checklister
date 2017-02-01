all: ico resize icns

icns:
	iconutil -c icns -o checklister.icns "/Users/psilotum/Documents/Dropbox/applications/checklister/src/icons/checklister.iconset"

ico:
	sips -z 256 256 checklister_icons_orig.png --out checklister_small.png
	convert checklister_small.png checklister.ico

resize:
	sips -z 2048 2048 checklister_icons_orig.png --out icon_2048x2048.png
	sips -z 16 16     icon_2048x2048.png --out checklister.iconset/icon_16x16.png
	sips -z 32 32     icon_2048x2048.png --out checklister.iconset/icon_16x16@2x.png
	sips -z 32 32     icon_2048x2048.png --out checklister.iconset/icon_32x32.png
	sips -z 64 64     icon_2048x2048.png --out checklister.iconset/icon_32x32@2x.png
	sips -z 128 128   icon_2048x2048.png --out checklister.iconset/icon_128x128.png
	sips -z 256 256   icon_2048x2048.png --out checklister.iconset/icon_128x128@2x.png
	sips -z 256 256   icon_2048x2048.png --out checklister.iconset/icon_256x256.png
	sips -z 512 512   icon_2048x2048.png --out checklister.iconset/icon_256x256@2x.png
	sips -z 512 512   icon_2048x2048.png --out checklister.iconset/icon_512x512.png
	sips -z 1024 1024   icon_2048x2048.png --out checklister.iconset/icon_512x512@2x.png
	sips -z 1024 1024   icon_2048x2048.png --out checklister.iconset/icon_1024x1024.png

clean:
	rm -rf checklister.iconset/*

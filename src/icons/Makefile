icns:
	iconutil -c icns checklister.iconset

ico:
	convert -resize 256x256 checklister_icons_orig.png checklister_small.png 
	convert -resize 2048x2048 checklister_icons_orig.png checklister.iconset/icon_2048x2048.png
	convert checklister_small.png checklister.ico

# you need to install imagemagick first 
resize:
	cd checklister.iconset;
	cp checklister.iconset/icon_2048x2048.png checklister.iconset/icon_2048x2048@2.png
	convert -resize 1024x1024 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_1024x1024.png
	cp checklister.iconset/icon_1024x1024.png checklister.iconset/icon_1024x1024@2.png
	convert -resize 512x512 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_512x512.png
	cp checklister.iconset/icon_512x512.png checklister.iconset/icon_512x512@2.png
	convert -resize 256x256 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_256x256.png
	cp checklister.iconset/icon_256x256.png checklister.iconset/icon_256x256@2.png
	convert -resize 128x128 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_128x128.png
	cp checklister.iconset/icon_128x128.png checklister.iconset/icon_128x128@2.png
	convert -resize 64x64 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_64x64.png
	cp checklister.iconset/icon_64x64.png checklister.iconset/icon_64x64@2.png
	convert -resize 32x32 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_32x32.png
	cp checklister.iconset/icon_32x32.png checklister.iconset/icon_32x32@2.png
	convert -resize 16x16 checklister.iconset/icon_2048x2048.png checklister.iconset/icon_16x16.png
	cp checklister.iconset/icon_16x16.png checklister.iconset/icon_16x16@2.png

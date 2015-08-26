icns:
	iconutil -c icns ngenerator.iconset

ico:
	convert -resize 256x256 ngenerator_icons_orig.png ngenerator_small.png 
	convert ngenerator_small.png ngenerator.ico

# you need to install imagemagick first 
resize:
	cd ngenerator.iconset;
	cp ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_2048x2048@2.png
	convert -resize 1024x1024 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_1024x1024.png
	cp ngenerator.iconset/icon_1024x1024.png ngenerator.iconset/icon_1024x1024@2.png
	convert -resize 512x512 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_512x512.png
	cp ngenerator.iconset/icon_512x512.png ngenerator.iconset/icon_512x512@2.png
	convert -resize 256x256 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_256x256.png
	cp ngenerator.iconset/icon_256x256.png ngenerator.iconset/icon_256x256@2.png
	convert -resize 128x128 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_128x128.png
	cp ngenerator.iconset/icon_128x128.png ngenerator.iconset/icon_128x128@2.png
	convert -resize 64x64 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_64x64.png
	cp ngenerator.iconset/icon_64x64.png ngenerator.iconset/icon_64x64@2.png
	convert -resize 32x32 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_32x32.png
	cp ngenerator.iconset/icon_32x32.png ngenerator.iconset/icon_32x32@2.png
	convert -resize 16x16 ngenerator.iconset/icon_2048x2048.png ngenerator.iconset/icon_16x16.png
	cp ngenerator.iconset/icon_16x16.png ngenerator.iconset/icon_16x16@2.png

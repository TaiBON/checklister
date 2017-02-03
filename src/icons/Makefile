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

toolbar:
	convert -resize 1024x1024 addspecies.svg     -transparent white addspecies.png
	convert -resize 1024x1024 addspecies.svg     -transparent white addspecies@2x.png
	convert -resize 1024x1024 batch.svg          -transparent white batch.png
	convert -resize 1024x1024 batch.svg          -transparent white batch@2x.png
	convert -resize 1024x1024 bug_report.svg     -transparent white bug_report.png
	convert -resize 1024x1024 bug_report.svg     -transparent white bug_report@2x.png
	convert -resize 1024x1024 delete.svg         -transparent white delete.png
	convert -resize 1024x1024 delete.svg         -transparent white delete@2x.png
	convert -resize 1024x1024 delete_all.svg     -transparent white delete_all.png
	convert -resize 1024x1024 delete_all.svg     -transparent white delete_all.png
	convert -resize 1024x1024 deselect.svg     -transparent white deselect@2x.png
	convert -resize 1024x1024 deselect.svg     -transparent white deselect.png
	convert -resize 1024x1024 execute_export.svg -transparent white execute_export.png
	convert -resize 1024x1024 execute_export.svg -transparent white execute_export@2x.png
	convert -resize 1024x1024 export.svg         -transparent white export.png
	convert -resize 1024x1024 export.svg         -transparent white export@2x.png
	convert -resize 1024x1024 home.svg           -transparent white home.png
	convert -resize 1024x1024 home.svg           -transparent white home@2x.png
	convert -resize 1024x1024 nomenmatch.svg     -transparent white nomenmatch.png
	convert -resize 1024x1024 nomenmatch.svg     -transparent white nomenmatch@2x.png
	convert -resize 1024x1024 save_txt.svg       -transparent white save_txt.png
	convert -resize 1024x1024 save_txt.svg       -transparent white save_txt@2x.png
	convert -resize 1024x1024 search.svg         -transparent white search.png
	convert -resize 1024x1024 search.svg         -transparent white search@2x.png
	convert -resize 1024x1024 tropicos.svg       -transparent white tropicos.png
	convert -resize 1024x1024 tropicos.svg       -transparent white tropicos@2x.png

clean:
	rm -rf checklister.iconset/*

all:
	pyuic4 ui/namegen.ui -o ui_window.py

macos:
	py2applet --make-setup NGenerator.py
	python3 setup.py py2app --includes "sip"

clean:
	rm -fr build dist

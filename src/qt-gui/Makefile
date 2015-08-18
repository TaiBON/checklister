PYUIC=pyuic5
PYTHON=python3

all:
	$(PYUIC) ui/namegen.ui -o ui_window.py

macos:
	py2applet --make-setup NGenerator.py
	$(PYTHON) setup.py py2app --includes "sip"

clean:
	rm -fr build dist

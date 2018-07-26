PYUIC = pyuic4
REINDENT = reindent.py

SOURCES = __init__.py \
	economicdiameter.py \
	EpanetModel.py \
	EpanetResultReader.py \
	GHydraulicsCommon.py \
	GHydraulicsException.py \
	GHydraulicsInpReader.py \
	GHydraulicsInpWriter.py \
	GHydraulicsModel.py \
	GHydraulicsModelChecker.py \
	GHydraulicsModelMaker.py \
	GHydraulicsModelRunner.py \
	ghydraulicsplugin.py \
	GHydraulicsResultDialog.py \
	GHydraulicsSettingsDialog.py \
	ghyeconomicdiameter.py
	
GENERATED = resources.py \
	Ui_GHydraulicsResultDialog.py \
	Ui_GHydraulicsSettingsDialog.py
 
dist-zip: ghydraulic.zip

ghydraulic.zip: $(SOURCES) $(GENERATED)
	-rm ghydraulic.zip
	find . -name "*~" -exec rm {} \;
	find . -name "*.bak" -exec rm {} \;
	cd ..;zip ghydraulic/ghydraulic.zip ghydraulic/*.py ghydraulic/*.png \
	ghydraulic/*.xpm ghydraulic/AUTHORS ghydraulic/COPYING \
	ghydraulic/etc/* \
	ghydraulic/Makefile ghydraulic/README ghydraulic/TODO \
	ghydraulic/metadata.txt ghydraulic/icons/* \
	ghydraulic/samples/d-w/cmd/* ghydraulic/samples/d-w/lps/* \
	ghydraulic/samples/h-w/gpm/* \
	ghydraulic/src/* ghydraulic/bin/32bit/ELF/* \
	ghydraulic/bin/32bit/WindowsPE/* ghydraulic/bin/64bit/ELF/* \
	ghydraulic/bin/64bit/WindowsPE/* ghydraulic/bin/osx/* 

indent: $(SOURCES)
	$(REINDENT) $(SOURCES)

Ui_GHydraulicsResultDialog.py: result.ui
	$(PYUIC) -o Ui_GHydraulicsResultDialog.py result.ui
	
Ui_GHydraulicsSettingsDialog.py: settings.ui
	$(PYUIC) -o Ui_GHydraulicsSettingsDialog.py settings.ui
	
clean:
	-rm Ui_*
	-rm ghydraulic.zip

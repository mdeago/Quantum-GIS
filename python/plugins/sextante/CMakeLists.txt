SET (SEXTANTE_PLUGIN_DIR ${QGIS_DATA_DIR}/python/plugins/sextante)

ADD_SUBDIRECTORY(admintools)
ADD_SUBDIRECTORY(algs)
ADD_SUBDIRECTORY(core)
ADD_SUBDIRECTORY(gdal)
ADD_SUBDIRECTORY(grass)
ADD_SUBDIRECTORY(gui)
ADD_SUBDIRECTORY(images)
ADD_SUBDIRECTORY(lidar)
ADD_SUBDIRECTORY(modeler)
ADD_SUBDIRECTORY(otb)
ADD_SUBDIRECTORY(outputs)
ADD_SUBDIRECTORY(parameters)
#ADD_SUBDIRECTORY(pymorph)
ADD_SUBDIRECTORY(r)
ADD_SUBDIRECTORY(saga)
ADD_SUBDIRECTORY(script)
ADD_SUBDIRECTORY(taudem)
ADD_SUBDIRECTORY(tools)
#ADD_SUBDIRECTORY(tests)

FILE(GLOB UI_FILES ui/*.ui)
PYQT4_WRAP_UI(PYUI_FILES ${UI_FILES})

FILE(GLOB OTHER_FILES metadata.txt)
FILE(GLOB PY_FILES *.py)

PYQT4_ADD_RESOURCES(PYRC_FILES resources.qrc)

PLUGIN_INSTALL(sextante . ${PY_FILES} ${OTHER_FILES} ${PYRC_FILES})
PLUGIN_INSTALL(sextante ui ${PYUI_FILES} ui/__init__.py)

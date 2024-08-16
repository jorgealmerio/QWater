@ECHO OFF
 
set OSGEO4W_ROOT=C:\OSGeo4W
 
set PATH=%OSGEO4W_ROOT%\bin;%PATH%
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
 
@echo off
call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
@echo off
::path %OSGEO4W_ROOT%\apps\qgis\bin;%OSGEO4W_ROOT%\apps\grass\grass78\lib;%OSGEO4W_ROOT%\apps\grass\grass78\bin;%PATH%
 
cd /d %~dp0
 
@ECHO ON
::Ui Compilation
::call pyuic5 multi_ring_buffer_dialog_base.ui -o multi_ring_buffer_dialog_base.py          
 
::Resources
::call pyrcc5 resources.qrc -o resources.py
:: https://manpages.ubuntu.com/manpages/focal/man1/pylupdate5.1.html  -noobsolete -tr-function <name> -translate-function <name>
call pylupdate5 i18n\QWater.pro -verbose -noobsolete ::-tr-function tr -translate-function QCoreApplication.translate
 
::@ECHO OFF
GOTO END
 
:ERROR
   echo "Failed!"
   set ERRORLEVEL=%ERRORLEVEL%
   pause
 
:END
@ECHO ON
@echo off 

echo ===================================

echo =======MY_TOOLS INSTALLATION=======

echo =================================== 
 
#START /WAIT %~dp0\Temp\PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x64.exe

cd c:\ 
START /WAIT pip install pyinstaller
echo "First Step Complete"

cd %~dp0\Temp
START /WAIT pyinstaller -w -F dHalley_ArtProof_MenuGenerator.py
echo "Second Step Complete"

rem COPY "%~dp0\Temp\dist\FileNamer.exe" "%systemdrive%\users\%username%\Desktop\FileNamer.exe" 
rem echo "Third Step Complete"

@echo off
echo msgbox "Installation Complete." > "%temp%\popup.vbs"
wscript.exe "%temp%\popup.vbs"




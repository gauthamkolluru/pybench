:START
REM Requirement: Open with an Elevated Administrator CMD Window
@echo off
setlocal
set MSFTLOGS=%temp%\MSFTLOGS
if not exist %MSFTLOGS% (
mkdir %MSFTLOGS% 2>nul
)
echo "Hit Enter to collect Event logs"
@pause
@echo.
echo Gathering Event logs
copy %windir%\System32\winevt\Logs\Application.evtx %MSFTLOGS% /y
copy %windir%\System32\winevt\Logs\System.evtx %MSFTLOGS% /y
SETLOCAL ENABLEDELAYEDEXPANSION
SET sourceDirPath=%MSFTLOGS%
IF [%2] EQU [] (
SET destinationDirPath="%USERPROFILE%\AppData\Local\Temp\MSFTLOGS"
) ELSE (
SET destinationDirPath="%2"
)
IF [%3] EQU [] (
SET destinationFileName="MSFT_logs.cab"
) ELSE (
SET destinationFileName="%3"
)
SET tempFilePath=%TEMP%\FilesToZip.txt
TYPE NUL > %tempFilePath%FOR /F "DELIMS=*" %%i IN ('DIR /B /S /A-D "%sourceDirPath%"') DO (SET filePath=%%i
SET dirPath=%%~dpi
SET dirPath=!dirPath:~0,-1!
SET dirPath=!dirPath:%sourceDirPath%=!
SET dirPath=!dirPath:%sourceDirPath%=!
ECHO .SET DestinationDir=!dirPath! >> %tempFilePath%
ECHO "!filePath!" >> %tempFilePath%
)
MAKECAB /D MaxDiskSize=0 /D CompressionType=MSZIP /D Cabinet=ON /D Compress=ON /D UniqueFiles=OFF /D DiskDirectoryTemplate=%destinationDirPath% /D CabinetNameTemplate=%destinationFileName%  /F %tempFilePath% > NUL 2>&1

echo click Continue to delete Event logs from the TEMP folder"
@pause
@echo.
del %temp%\MSFTLOGS\Application.evtx
del %temp%\MSFTLOGS\System.evtx

@echo.
echo Click enter to open the Temp logs file location...
start %temp%\MSFTLOGS
:END

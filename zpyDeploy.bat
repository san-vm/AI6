rmdir /S /Q __pycache__
rmdir /S /Q build
rmdir /S /Q dist
rmdir /S /Q AI

cls
@REM pyinstaller --noconsole --icon=zImg\promodders.ico sysTrayApp.py -n AI
pyinstaller AIUI.spec

move dist\AI AI
xcopy /E /y Lib\site-packages\vosk AI\vosk\
xcopy /E /y Lib\site-packages\pvporcupine AI\pvporcupine\
xcopy /E /y Lib\site-packages\cv2\data AI\cv2\data\
xcopy /E /y model AI\model\
xcopy /E /y zImg AI\zImg\
copy ffmpeg.exe AI\


rmdir /S /Q dist
rmdir /S /Q __pycache__
rmdir /S /Q build

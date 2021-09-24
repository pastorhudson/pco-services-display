pyinstaller -F ..\main.py -n get_report
move .\dist\get_report.exe ..\get_report.exe
rmdir /S /Q .\build
rmdir /S /Q .\dist
del .\*.spec
pyinstaller -F ../main.py -n get_report
chmod +x get_report
mv ./dist/get_report ../
rm -R ./dist
rm -R ./build
rm ./*.spec

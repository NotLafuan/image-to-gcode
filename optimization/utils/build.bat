@echo off
cls
echo python setup.py build
python setup.py build
del myModule.cp310-win_amd64.pyd
copy build\lib.win-amd64-cpython-310\myModule.cp310-win_amd64.pyd myModule.cp310-win_amd64.pyd
echo.
echo python test.py
python test.py
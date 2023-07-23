@echo off
cls
echo python setup.py build
python setup.py build
del myModule.cp311-win_amd64.pyd
copy build\lib.win-amd64-cpython-311\myModule.cp311-win_amd64.pyd myModule.cp311-win_amd64.pyd
echo.
echo python test.py
python test.py
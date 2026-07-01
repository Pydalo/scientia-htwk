:;# !/usr/bin/env bash
:; exec ./scientia/.venv/bin/python ./scientia/scientia.py "$@"
@echo off
"%~dp0\scientia\.venv\Scripts\python.exe" "%~dp0\scientia\scientia.py" %*
exit /b 0
    
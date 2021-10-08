echo %~dp0
"..\python\pythonw.exe" -m "{{ cookiecutter.module_name }}" "%1"
pause
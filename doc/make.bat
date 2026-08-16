@ECHO OFF
pushd %~dp0
if "%SPHINXBUILD%" == "" ( set SPHINXBUILD=sphinx-build )
set SOURCEDIR=source
set BUILDDIR=build
if "%1" == "" goto help
if "%1" == "check" goto check
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end
:check
%SPHINXBUILD% -b html -n -W --keep-going %SOURCEDIR% %BUILDDIR%\html %SPHINXOPTS% %O%
goto end
:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
:end
popd

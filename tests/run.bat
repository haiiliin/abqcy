REM Change directory to the directory of this file
cd /D "%~dp0"

REM Compile the subroutines
if not exist subs mkdir subs
cd subs
python3.11 ..\..\abqcy\__main__.py compile ..\..\abqcy\subroutines\elastic.pyx
cd ..

REM Run the job
set inp=column.inp
set sub=elastic-std.obj
set job=Job-column-elastic
if not exist jobs\%job% mkdir jobs\%job%
echo F|xcopy subs\%sub% jobs\%job%\%sub% /Y
echo F|xcopy inputs\%inp% jobs\%job%\%inp% /Y
cd jobs\%job%
abaqus job=%job% input=%inp% user=%sub% interactive
cd ..\..

REM Change directory to the directory of this file
cd /D "%~dp0"

pip install ..
abqcy run --job=Job-column-elastic --input=inputs/column.inp --user=../abqcy/subroutines/elastic.pyx --output=jobs/Job-column-elastic

REM Change directory to the directory of this file
cd /D "%~dp0"

pip install ..
abqcy run --job=Job-element-elastic --model=models/element.py --user=../examples/elastic.py --output=jobs/Job-element-elastic --post=models/element-output.py --visualization=models/element-visualization.py
xcopy jobs\Job-element-elastic\U3.* outputs\elastic\ /C /S /D /Y /I

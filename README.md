# DriverMonitoringSystem


## Instruction to run the application

The developed DMS application contains different modules like ***driverMonitoring.py*** as the main 
module, ***faceDetect.py*** for face detection, and ***calculations.py*** for the calculation of ***ADR*** and ***MAR***. 
Other modules include ***headPostionEstimation.py*** for estimating the head position of the driver, 
***faceGeometry.py*** which contains the 3D real-world coordinates of a generic model, and 
***eyeLongClosedDetection.py*** for detecting the eye state and raising a warning if necessary. The final 
module is the ***yawnDetection.py*** to detect the mouth state and yawn. 

### Creating and activating the virtual Environment

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\activate

```
### Running application in venv
```
python driverMonitoring.py
```

### Quiting the application
```
press 'q'
```
### Raspberry PI
Same process as above but for mediapipe 
```
sudo pip3 install mediapipe-rpi3

or 

sudo pip3 install mediapipe-rpi4
```
Additional packages if needed can be found at https://pypi.org/project/mediapipe-rpi3/#description

## Instruction to Generate Documentation
 
Install sphinx using pip 
```
 pip install sphinx
 pip install sphinx_rtd_theme
 
 cd docs
 make html
```

The documentation will be generated in ***docs/_build/html/index.html***




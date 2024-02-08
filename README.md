# DriverMonitoringSystem


## Instruction to run the application

The developed DMS application contains different modules like ***driverMonitoring.py*** as the main 
module, ***faceDetect.py*** for face detection, and ***calculations.py*** for the calculation of ***ADR*** and ***MAR***. 
Other modules include ***headPostionEstimation.py*** for estimating the head position of the driver, 
***faceGeometry.py*** which contains the 3D real-world coordinates of a generic model, and 
***eyeLongClosedDetection.py*** for detecting the eye state and raising a warning if necessary. The final 
module is the ***yawnDetection.py*** to detect the mouth state and yawn. 

For the application to run on a PC, the packages like mediapipe, opencv-python, scipy, numpy, etc. are 
installed. These packages are installed using the **pip install -r requirements.txt** command. If any missing packages can be installed using **pip install <package_name>** Then  
the DMS application can be run through the command prompt using the command ***python driverMonitoring.py*** and can be quitted by key ‘q’

In Raspberry Pi, the installation of the packages is similar to PC using **pip3 install *package_name*** except for the mediapipe package which can be installed using the command ***sudo pip3 install mediapipe-rpi3*** for Raspberry Pi 3 and ***sudo pip3 install mediapipe-rpi4*** for the Raspberry Pi 4.  Additional packages if needed can be found at https://pypi.org/project/mediapipe-rpi3/#description

## Instruction to Generate Documentation
 
Install sphinx using pip 
```
 pip install sphinx
 pip install sphinx_rtd_theme
 
 cd docs
 make html
```

The documentation will be generated in ***docs/_build/html/index.html***




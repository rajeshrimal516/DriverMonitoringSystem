.. Driver Monitoring System documentation master file, created by
   sphinx-quickstart on Sun Jun 25 10:41:12 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Driver Monitoring System's documentation!
====================================================

*************
Introduction:
*************

A driver monitoring system (DMS) is a technology designed to monitor and assess the driver's behavior, attention, and alertness while operating a vehicle. It utilizes a combination of sensors, cameras, and advanced algorithms to detect and analyze various driver-related parameters in real-time. These parameters may include eye movements, head position, facial expressions, body posture, and even vital signs.

-----------
Importance:
-----------

1. Enhanced Safety: The primary objective of a driver monitoring system is to improve safety on the roads. By continuously monitoring the driver's behavior, it can detect signs of drowsiness, distraction, or impairment. It can then issue warnings or alerts to bring the driver's attention back to the road, potentially preventing accidents caused by human error.

2. Fatigue and Distraction Detection: Drowsy driving and driver distraction are major contributors to road accidents. A DMS can analyze eye movements, blinking patterns, and head position to detect signs of drowsiness or driver inattention. By alerting the driver when such behavior is detected, it can help reduce the risk of accidents caused by fatigue or distractions.

3. Real-time Driver Assistance: In addition to monitoring the driver, some DMS implementations can provide real-time assistance. For example, if the system detects that the driver is not paying attention to the road ahead, it can trigger an alert or even take control of the vehicle momentarily to avoid a potential collision.

4. Personalized Safety Features: Driver monitoring systems can adapt to individual driver characteristics and preferences. By continuously monitoring and analyzing data, the system can learn the driver's typical behavior and identify deviations from the norm. This allows for personalized safety features and interventions tailored to the specific needs of the driver.

5. Fleet Management: DMS technology is particularly valuable for fleet operators. It enables them to monitor their drivers' performance, detect risky behavior, and provide targeted training or intervention when necessary. This can help improve overall fleet safety, reduce operational costs, and protect the reputation of the company.

6. Regulatory Compliance: Many regions and countries have started to mandate the use of driver monitoring systems in certain types of vehicles. Compliance with these regulations ensures that vehicles meet the required safety standards and contributes to a safer transportation ecosystem.

In conclusion, driver monitoring systems play a crucial role in enhancing road safety by continuously monitoring and analyzing driver behavior. By detecting signs of fatigue, distraction, or impairment, these systems can help prevent accidents and improve the overall driving experience. As technology continues to advance, driver monitoring systems are expected to become more sophisticated, leading to safer roads and a reduction in preventable accidents.

Developed DMS
=============

The developed DMS application contains different modules like **driverMonitoring.py** as the main 
module, **faceDetect.py** for face detection, and **calculations.py** for calculation of **ADR** and **MAR**. 
Other modules include **headPostionEstimation.py** for estimating the head position of the driver, 
**faceGeometry.py** which contains the 3D real-world coordinates of a generic model, and 
**eyeLongClosedDetection.py** for detecting the eye state and raising warning if necessary. The final 
module is the **yawnDetection.py** to detect the mouth state and yawn. 

For the application to run on PC, the packages like mediapipe, opencv-python, scipy, numpy, etc. are 
installed. These packages are installed using the **pip install package_name** command. Then after 
the DMS application can be run through the command prompt using the command **python 
driverMonitoring.py** and can be quitted by key q.

In Raspberry Pi, the installation of the packages is similar to PC using **pip3 install package_name** except for the mediapipe package which can be installed using the command **sudo pip3 install mediapipe-rpi3** for Raspberry Pi 3 and **sudo pip3 install mediapipe-rpi4** for the Raspberry Pi 4.  Additional packages if needed can be found in https://pypi.org/project/mediapipe-rpi3/#description

The whole documentation of this developed DMS is available on the https://urn.nsk.hr/urn:nbn:hr:200:034698. 

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   driverMonitoring
   common
   facedetect
   head_pos_estimator
   calculations
   yawn_detector
   eyelongclosed_detector

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Driver Monitoring System
Copyright (c) 2023, Rajesh Rimal. All rights reserved.

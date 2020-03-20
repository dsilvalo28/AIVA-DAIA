# AIVA-DAIA
## Industrial and Commercial Applications - Tree detection in aerial images

Application that measures the percentage and square meters of tree mass and the number of trees in an aerial image of a city.

## Installation 
- Have Python installed on your computer.
- Download the project from the git link and open it in your programming environment, for example PyCharm.
- Install the libraries specified in the requirements.txt file.
- Create a file called credentials.py with GOOGLE_MAPS_API_KEY = 'Your_Google_API_Key' to have it locally.
- Change directory to AIVA-DAIA.
### Tests
  Run: 
  `python -m unittest`
  
  If you wanna see the output:
  `DEBUG=True python -m unittest`
  
  If credentials.py is not created:
  `GOOGLE_MAPS_API_KEY=Your_Google_API_Key python -m unittest`
  
### Application:
- Change self.run() in the init class to try different inputs and then execute: 
  
  `python -m src.Application`

**Warning**: Debug option and application might lock the process while showing the result windows.


## Requirements
- Python 3.7.4
- OpenCV 4.2.0.32
- Numpy 1.18.1
- Matplotlib 3.2.1

## Authors
- Daniel Hernández Ferrándiz
- Diego Silva López

This is the implementation of ConPrEF for testing.
## Cite
```
@inproceedings{sirigu2023conpref,
  title={ConPrEF: a context-based privacy enforcement framework for edge computing},
  author={Sirigu, Giorgia and Carminati, Barbara and Ferrari, Elena},
  booktitle={2023 IEEE International Conference on Edge Computing and Communications (EDGE)},
  pages={72--78},
  year={2023},
  organization={IEEE}
}
```
# Getting Started

## Requirements
- Python 3.10+ 
 - pygeodesy ("pip install PyGeodesy")
 - openpyxl ("pip install openpyxl")
 - jpype ("pip install JPype1" or "pip install py4j" or "pip install pyjnius==1.4.1")
- Docker
- RaspberryPi[^1] (not mandatory)

## Implementation Structure
This implementation provides two different testing settings.
The one in "smartphone" folder runs the client application through a docker container, while the one in "smartwatch" runs directly within the device (or Raspberry). 

# Run the System
At first you have to start the server:
1. open the terminal
2. enter folder `cd edge`
3. run command `python3 edgeServer.py`

Running the **Smartwatch** application:
1. open the terminal
2. enter folder `cd smartwatch`
3. run command `python3 testSmartwatch.py`
The results of the test are stored within the folder `TestingResultsSmartwatch`, that is generated after the first execution.

Running the **Smartphone** application:
1. open the terminal
2. enter folder `cd smartphone`
3. run command to build the image `docker build -t device-image .`
4. run the command to start the application container `docker run -dp 8080:8080 --network host --name device --cpus 8 -m 8g -v $(pwd)/TestingResultsSmartphone:/src/device/TestingResults device-image`

The results of the test are stored within the folder `TestingResultsSmartphone`, that is generated after the first execution.

[^1]: https://www.raspberrypi.com/

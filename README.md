# pgarmyn/ecowitt_net

This module provides a simple interface to retrieve real-time or historical 
device data from ecowitt.net, a data hosting service for ECOWITT meteostations.

DEPENDENCIES :

A connection to the ecowitt.net server can only be established with : 
- a valid Api key
- a valid Application key
- a valid MAC address of Ecowitt meteostation, 
   the meteostation must be active if real-time data is requested

Typically, the module is used to retrieve data from a propietary meteostation.
In that case, keys can be created in https://www.ecowitt.net/user/index, 
after login.

The module has been written and tested with Python 3.9
Other packages : 
- requests
- datetime

For more information on parameters, you can consult the documentation of the Ecowitt API :
https://doc.ecowitt.net/web/#/apiv3en?page_id=1

USE :

- edit "ecowitt_my_param.py" to set your keys and MAC address
- edit "ecowitt_my_param.py" UnitsEcowitt to modify the units for 
      retrieved values
- use function "ecowitt_get_realtime" to retriev real-time data
- use function "ecowitt_get_history" to retriev history data
- 
EXEMPLES :
 
See "exemple.py" for examples

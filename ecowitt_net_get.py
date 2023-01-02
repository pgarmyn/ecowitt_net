import requests
from datetime import datetime
from ecowitt_my_param import *

#Ecowitt documentation  : https://doc.ecowitt.net/web/#/apiv3en?page_id=1
HTTPS_Ecowitt_REALTIME = f'https://api.ecowitt.net/api/v3/device/real_time?application_key={ApplicationKey}&api_key={ApiKey}&mac={MAC_station}&call_back='
HTTPS_Ecowitt_HISTORY = f'https://api.ecowitt.net/api/v3/device/history?application_key={ApplicationKey}&api_key={ApiKey}&mac={MAC_station}&call_back='

KEY_SEPARATOR = '.'

def _t2dt(t):
    """Convert epoch time to datetime"""
    if isinstance(t, str):
        t = int(t)
    return datetime.fromtimestamp(t)


# Flatten dict ,  keep1level=True  to keep last level as  {'time': datetime.datetime(2022, 12, 31, 17, 23, 31), 'unit': '℃', 'value': '27.4'}
# Time in datetime format


def _response_realtime_to_dict(resp, parent_key: str = '') -> dict:
    """Convert requests.Response to dict, format time as datetime, convert string-numbers to float
     see also https://doc.ecowitt.net/web/#/apiv3en 'Getting Device Real-Time Data'"""

    data = resp if isinstance(resp, dict) else dict(resp.json())
    items = []
    for k, v in data.items():
        new_key = parent_key + KEY_SEPARATOR + k if parent_key else k
        if isinstance(v, dict):
            if any (k1 in {'value','unit'} for k1 in v.keys()):
                if 'time' in v.keys():
                    v['time'] = _t2dt(v['time'])
                if 'value' in v.keys():
                    v['value'] = float(v['value'])
                items.append((new_key, v))
            else:
                items.extend(_response_realtime_to_dict(v, new_key).items())
        else:
            if k == 'time':
                v = _t2dt(float(v))
            items.append((new_key, v))
    return dict(items)


def _response_history_to_dict(resp, parent_key: str = '') -> dict:
    """Convert requests.Response to dict, format time as datetime, convert string-numbers to float
    see also https://doc.ecowitt.net/web/#/apiv3en 'Getting Device History Data'"""

    items = []
    data = resp if isinstance(resp, dict) else dict(resp.json())
    for k, v in data.items():
        new_key = parent_key + KEY_SEPARATOR + k if parent_key else k
        #print('items, item : ', k, new_key,  v)
        if k in ['list', 'code']:
            items.append((new_key, v))
        elif k == 'time':
            v = _t2dt(v)
            items.append((new_key, v))
        elif isinstance(v, dict):
            if 'list' in v.keys():
                data_dict = v['list']
                for k1 in list(data_dict.keys()):
                    k_new = _t2dt(k1)
                    data_dict[k_new] = float(data_dict.pop(k1))
                v['list'] = data_dict
                items.append((new_key, v))
            else:
                items.extend(_response_history_to_dict(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def ecowitt_get_realtime(call_back: str = 'all', units: str = UnitsEcowitt) -> dict:
    """Get realtime data from Ecowitt.net, as dict.

     'ApiKey', 'ApplicationKey', 'MAC_station' and 'UnitsEcowitt' : defined in ecowitt_my_param.py;
     'call-back', 'units' : see https://doc.ecowitt.net/web/#/apiv3en "Getting Device Real-Time Data"

    :rtype: dict
    :param call_back: 'all' (default) or a selection 'outdoor.temperature,indoor.temperature'
    :param units: to override UnitsEcowitt
    :return: flatten dict or partial flatten dict
    """
    try:
        resp = requests.get(HTTPS_Ecowitt_REALTIME + call_back + units, timeout=80)
        return _response_realtime_to_dict(resp)
    except requests.exceptions.RequestException as err:
        print(f'ERROR : module {__name__}  with line : r = requests.get(https_ecowitt_realtime+call_back+units, timeout=80)\nERROR : {err}')
        return {'code': -1, 'msg': f'error : {str(err)}', 'time': datetime.now()}


def ecowitt_get_history(start_date: datetime, end_date: datetime, call_back: str, cycle_type: str = 'auto', units: str = UnitsEcowitt) -> dict:
    """Get history data from Ecowitt.net, as dict.

        'ApiKey', 'ApplicationKey', 'MAC_station' and 'UnitsEcowitt' : defined in ecowitt_my_param.py;
        'call-back', 'units' : see https://doc.ecowitt.net/web/#/apiv3en "Getting Device History Data"

        :param start_date: start date for retrieving data, sit Ecowitt.net docs for details
        :param end_date: end date for retrieving data, sit Ecowitt.net docs for details
        :param call_back: 'all' (default) or selection 'outdoor.temperature,indoor.temperature'
        :param cycle_type: 'auto' (default) or '5min','30min','4hour','1day'; possible values depend on timespan
        :param units: to override UnitsEcowitt
        :return: flatten dict or partial flatten dict
        :rtype: dict
        """
    try:
        timespan = '&start_date='+start_date.strftime('%Y-%m-%d %H:%M:%S')+'&end_date='+end_date.strftime('%Y-%m-%d %H:%M:%S')
        cycletype = f'&cycle_type={cycle_type}'
        resp = requests.get(HTTPS_Ecowitt_HISTORY + call_back + timespan + cycletype + units, timeout=80)
        return _response_history_to_dict(resp)
    except requests.exceptions.RequestException as err:
        print(f'ERROR : module {__name__}  with line : r = requests.get(https_ecowitt_history+call_back+timespan+cycletype,timeout=80)\nERROR : {err}')
        return {'code': -1, 'msg': f'error : {str(err)}', 'time': datetime.now()}

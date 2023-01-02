#!/usr/bin/python
from ecowitt_net_get import ecowitt_get_realtime, ecowitt_get_history
from time import sleep
from datetime import datetime,timedelta

"""
  exemple of retrieving personal data from ecowitt.net
"""

if __name__ == '__main__':

    do_realtime_all = True
    do_realtime_selection = True
    do_history = True

    if do_realtime_all :

        # EXEMPLE of retrieving real-time data from ecowitt.net

        # retrieve all real-time data from ecowitt.net as dict "data" with 1 nested level
        # data['data outdoor temperature'] = {'time': datetime.datetime(2022, 12, 31, 19, 16, 27), 'unit': '℃', 'value': 13.7}
        # ....

        data = ecowitt_get_realtime()

        # exemple of data access
        print('-'*90)
        print(1,'RETRIEVE ALL REAL-TIME DATA VALUES, as dictionary with 1 nested level (default):\n    {')
        [print('        ',key,':',value) for key, value in data.items()]
        print('    {\nPRINTING some INDIVIDUAL VALUES:')
        for k in ['data.outdoor.temperature', 'data.indoor.temperature']:
            print('    ',k, '=', data[k]['value'], data[k]['unit'])
        print('\nwill continue...\n')
        sleep(2)

    if do_realtime_selection:

        # retrieve selection of real-time data from ecowitt.net as dict "data" with 1 nested level
        # data['data outdoor temperature'] = {'time': datetime.datetime(2022, 12, 31, 19, 16, 27), 'unit': '℃', 'value': 13.7}
        # ....

        selection = 'outdoor.temperature,indoor.temperature'
        data = ecowitt_get_realtime(call_back=selection)

        # exemple of data access
        print('-'*90)
        print(2,f'RETRIEVE SELECTION ['+selection+'] of REAL-TIME DATA VALUES, as dictionary with  nested level :\n    {')
        [print('        ',key, ':', value) for key, value in data.items()]
        k = 'data.outdoor.temperature'
        print('    }\nPRINTING selection (' + k + ') of REAL-TIME VALUES :\n    ')
        print('    ',k, ':', data[k]['value'], data[k]['unit'])
        print('\nwill continue...\n')
        sleep(2)

    if do_history :
        # retrieve selection of historic data from ecowitt.net as dict "data" with double nested levels
        # data['data.outdoor.temperature'] = {'unit': '℃', 'list': {datetime: 13.7, datetime: 13.8, ...}}
        # ....
        selection = 'outdoor.temperature,indoor.temperature'
        start_date = (datetime.now() - timedelta(days=1)).replace(minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(minute=0, second=0, microsecond=0)

        data = ecowitt_get_history(start_date, end_date, call_back=selection, cycle_type='5min')

        # exemple of data access
        print('-'*90)
        print(3,'RETRIEVE SELECTION ['+selection+'] of HISTORIC DATA VALUES, as dictionary with double nested level:\n    {')
        [print('        ', key, ':', value) for key, value in data.items()]
        print('    {')

    print('\nEND\n')


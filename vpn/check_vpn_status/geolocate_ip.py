import requests
import json
import logging

# api key for looking up ip addresses
ip_geoloc_api_key = '183c67fde4684c1a87fd27ddfff3954e'

# i have a free account that gives 30K lookups a month. if we don't cache
# the ip address in the variable, then i would exhaust my allowance in 8 hours.
location_data = dict()


def get_my_ips_location(ip=''):
    global location_data
    my_ips_location = 'UNKNOWN'

    if ip != '':
        ip = f'&ip={ip}'

    try:
        # call ipgeolocation service to look up the location for my current external
        # ip. see 1PW for username and password if you don't specify an ip address to
        # look up the location for, it just uses your ip we set a time out of a little
        # more than 3 seconds because that's what `requests` instructions say to do
        #
        resp = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={ip_geoloc_api_key}{ip}', timeout=3.05)

        location_data = json.loads(resp.content)
        my_ips_location = location_data['country_code2']

    except Exception as e:
        logging.debug(f'ERROR: looking up geolocation {e}')

    return my_ips_location

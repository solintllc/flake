#!/usr/bin/env python3


# notes
# - needs to run continuously. trying to start it once a second would be wasteful of CPU. plus, the results often take longer than a second to get a return
# - this script executes a loop which looks up current external IP address. if it's not the same as last time, it gets the geolocation. if it is the same, it does 
#   reports the same geolocation
# - the script reports it to a file in Library/Caches for the bitbar script to pick up


# set up logging
import logging
import requests
import os
import signal
import json
import flag


# GLOBALS AND CONSTANTS

# for the first go round, set to an obviously internal address
my_ip_address = '127.0.0.1'
# api key for looking up ip addresses
ip_geoloc_api_key = '183c67fde4684c1a87fd27ddfff3954e'

cache_dir = "/Users/rr/Library/Caches/Flake"
cache_file_my_ip_location = f'{cache_dir}/my_ips_location.txt'


def handler(signum, frame):
    logging.debug('All done')
    os._exit(0)


# returns true if my_ip_address has changed
def is_ip_address_changed():
    global my_ip_address

    try:
        # ipify says you can do millions of calls a second to this free endpoint if you want to
        resp = requests.get("https://api.ipify.org?format=plain", timeout = 3.05)
        logging.debug(f'old ip: {my_ip_address}. new ip: {resp.content}')
    except Exception as e:
        logging.debug(f'ERROR: Unable to look up ip address {e}')
        return True

    if resp.content != my_ip_address:
        my_ip_address = resp.content
        return True
    else:
        return False


locations = dict()
def get_my_ips_location():
    my_ips_location = 'UNKNOWN'

    try:
        if my_ip_address in locations:
            return locations[my_ip_address]
        else:
            # call ipgeolocation service to look up the location for my current external ip. see 1PW for username and password
            # if you don't specify an ip address to look up the location for, it just uses your ip
            # we set a time out of a little more than 3 seconds because that's what `requests` instructions say to do
            # 
            # i have a free account that gives 30K lookups a month. if we we didn't cache the ip address in the variable, then i would 
            # exhaust my allowanced in 8 hours.
            resp = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={ip_geoloc_api_key}', timeout = 3.05)

            location_data = json.loads(resp.content)
            my_ips_location = location_data['country_code2']
            locations[my_ip_address] = my_ips_location

    except Exception as e:
        logging.debug(f'ERROR: looking up geolocation {e}')

    return my_ips_location

# bitbar checks to see if the last edit time is older than 5 seconds
# if it is, bitbar shows an error. this prevents the thing from failing silently
# to prevent it from erroring, we need to update every loop
def record_my_ips_location(my_ips_location):
    logging.debug(f"Country set to: {my_ips_location}")
    with open(cache_file_my_ip_location, "w") as f:
        f.write(flag.flag(my_ips_location))


def setup_environment():
    try:
        os.mkdir(cache_dir)
    except FileExistsError as e:
        pass

    logging.basicConfig(filename=f'{cache_dir}/check_vpn_status.log', filemode="w", level=logging.INFO)


def __main():

    setup_environment()

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


    my_ips_location = 'UNKNOWN'
    while True:
        if is_ip_address_changed():
            my_ips_location = get_my_ips_location()

        record_my_ips_location(my_ips_location)


__main()

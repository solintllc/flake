#!/usr/bin/env python3


# notes
# - needs to run continuously. trying to start it once a second would be wasteful
#   of CPU. plus, the results often take longer than a second to get a return
# - this script executes a loop which looks up current external IP address. if
#   it's not the same as last time, it gets the geolocation. if it is the same, it
#   reports the same geolocation
# - the script reports it to a file in Library/Caches for the xbar script to pick up

import logging
import requests
import os
import signal
import flag
import geolocate_ip
from pathlib import Path

# GLOBALS AND CONSTANTS

package_name = 'com.solintllc.flake.vpn.check_vpn_status'

# for the first go round, set to an obviously internal address
my_ip_address = '127.0.0.1'
cache_dir = str(Path.home()) + f'/Library/Caches/{package_name}'
cache_file_my_ip_location = f'{cache_dir}/my_ips_location.txt'



def handler(signum, frame):
    logging.info(f'Received signal{signum}. Exiting.')
    os._exit(0)


# returns true if my_ip_address has changed
def is_ip_address_changed():
    global my_ip_address

    try:
        # ipify says you can do millions of calls a second to this free endpoint if you want to
        resp = requests.get("https://api.ipify.org?format=plain", timeout=3.05)
        logging.debug(f'old ip: {my_ip_address}. new ip: {resp.content}')
    except Exception as e:
        logging.warning(f'WARNING: Unable to look up ip address {e}')
        return False

    if resp.content != my_ip_address:
        my_ip_address = resp.content
        return True
    else:
        return False


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

    logging.basicConfig(filename=f'{cache_dir}/check_vpn_status.log', filemode="w", level=logging.DEBUG)
    logging.info("Starting...")

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def main():

    setup_environment()

    my_ips_location = 'UNKNOWN'
    while True:
        if is_ip_address_changed():
            my_ips_location = geolocate_ip.get_my_ips_location() 

        record_my_ips_location(my_ips_location)

if __name__ == '__main__':
    main()

#!/usr/bin/env bash
# <bitbar.title>Title goes here</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Your Name</bitbar.author>
# <bitbar.author.github>your-github-username</bitbar.author.github>
# <bitbar.desc>Short description of what your plugin does.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies></bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>

package_name="com.solintllc.flake.vpn.check_vpn_status"
cache_dir="${HOME}/Library/Caches/${package_name}"
flag_file="${cache_dir}/my_ips_location.txt"


main() {

   # if the status has been modified in the last 5 seconds, show it
   # other wise blink an error

   if [[ ! -z "$( find ${flag_file} -mtime -5s )" ]]
   then
      cat ${flag_file}
   elif [[ $(( $(date +%S) % 2 )) -eq 1 ]]
   then
      echo "⚠️ "
      echo "---"
      echo "VPN STATUS ERROR"
   else
      echo " "
      echo "---"
      echo "VPN STATUS ERROR"
   fi
}

main

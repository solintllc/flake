#!/usr/bin/env bash

package_name="com.solintllc.flake.vpn.check_vpn_status"
launch_agent_file="${HOME}/Library/LaunchAgents/${package_name}.plist"
install_dir="${HOME}/.bin/check_vpn_status"
xbar_dir="${HOME}/Library/Application Support/xbar/plugins"
cache_dir="${HOME}/Library/Caches/${package_name}"
launch_agent_log_file="${cache_dir}/launch_agent.log"

confirm() {
   local question="${1}"

   local retval=2
   while [[ ${retval} -eq 2 ]]
   do
      read -p "${question} y/n " yn
      case $yn in
         [Yy]* ) retval=1;;
         [Nn]* ) retval=0;;
         * ) echo "Please answer y or n.";;
      esac
   done

   return ${retval}
}

# delete old stuff and start over
cleanup() {
   # stop the launchagent
   echo "Stopping launch agent ${launch_agent_file}."
   launchctl unload ${launch_agent_file}

   # launch agent
   echo "Deleting all launch agents with flake in the name."
   rm ${HOME}/Library/LaunchAgents/*flake*

   # xbar
   echo "Removing all xbar scripts named flake."
   rm "${xbar_dir}"/*flake*

   # bin
   echo "Deleting flake directory link in home bin directory."
   rm -rf "${install_dir}"

   # cache
   echo "Deleting cache directory."
   rm -r "${cache_dir}"

   echo "Cleanup Complete."

}

main() {

   [[ $1 == "-f" ]]&&cleanup

   # create cache dir
   mkdir -p "${cache_dir}"

   # copy the LaunchAgent and update the path to run check script and package name
   sed -e "s%HOME%${HOME}%" \
       -e "s%LAUNCHAGENTLOG%${launch_agent_log_file}%" \
       -e "s/PACKAGE/${package_name}/" \
       -e "s/VERSION/$(date +%Y%m%d.%H%M)/" \
       launch_agent.plist > ${launch_agent_file}
   chmod go-rwx ${launch_agent_file}

   # create install directory
   mkdir -p "${install_dir}"

   # install a virtual environment if there isn't one already
   if [[ ! -d "${install_dir}/venv" ]]
   then
      python3 -m 'virtualenv' "${install_dir}/venv"
   fi

   # enter the virutal environment and install the required python modules
   source "${install_dir}/venv/bin/activate"
   pip install -r requirements.txt

   # install the scripts
   cp *.py *.sh "${install_dir}"
   chmod 0700 "${install_dir}"/*.*

   # load launchagent once you have clicked yes in Knock Knock
   confirm "Good to load LaunchAgent?"
   if [[ $? -eq 1 ]]
   then
      launchctl unload ${launch_agent_file}
      launchctl load -w ${launch_agent_file}
   fi

   # install the script xbar uses
   cp xbar.sh "${xbar_dir}/vpn_check_flake.1s.sh"
   chmod 0700 "${xbar_dir}/vpn_check_flake.1s.sh"

}

set -x

main $*


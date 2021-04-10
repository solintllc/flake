this contraption has several parts

1. python script. see check_vpn_status.py for more details
2. run_check.sh script. basically a wrapper to the python that sets up the venv.
3. launchagent. this runs the python script continuously. see com.solintllc.flake.vpn.check_vpn_status.plist.

   validate the plist with `plutil -lint com.solintllc.flake.vpn.check_vpn_status.plist`

   to debug:
      launchctl print-disabled users/504/com.solintllc.flake.vpn.check_vpn_status.plist
      note that you have to use the user id, not the user name. the commands won't fail with the username, but they won't work.
      also note that you have to use the utilname.plist, not just utilname, in the commands. again, won't fail, but won't work.

   i think you can use launctl load/unload, but i had my best luck with just logging out and back in

   in the end, i didn't need to do anything as sudo or root

   the specs say you should put the script in /usr/local/libexec, but a) you need to be root to do that, b) it didn't seem necessary,
   and c) it didn't actually work.

4. xbar is the utility that puts the stuff in the menu bar. see
   - https://github.com/matryer/xbar

5. bitbar script. this script looks for the stuff the check_vpn_status.py spits out and reports it in the menu bar. see xbar.sh.


to install (from check_vpn_status directory):

`./setup.sh`


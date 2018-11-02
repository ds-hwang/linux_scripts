#!/bin/bash

ip=$1

adb disconnect $ip:22

echo "Connecting to $ip"

ssh-keygen -R $ip

ssh root@$ip 'stop powerd'

ssh root@$ip 'cras_test_client --volume 10'

ssh root@$ip 'cras_test_client --dump_server_info | grep "System Volume"'

cat ~/.android/adbkey.pub | ssh root@$ip 'android-sh -c "cat > /data/misc/adb/adb_keys"'

ssh root@$ip 'android-sh -c "restorecon /data/misc/adb/adb_keys 2> /dev/null && stop adbd && start adbd"'

sleep 2

adb connect $ip:22

sleep 2

adb devices

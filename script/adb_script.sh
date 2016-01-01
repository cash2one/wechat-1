#! /bin/sh
#
# adb_script.sh
# Copyright (C) 2015 john <john@forever>
#
# Distributed under terms of the MIT license.
#


while true;do
    adb shell input touchscreen tap 357 853
    sleep 2
    adb shell input touchscreen tap 49 96
    sleep 1
done

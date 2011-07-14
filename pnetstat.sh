#!/bin/sh
myvar1=`system_profiler SPAirPortDataType | grep -A 1 "Current Network Information:" | grep -v -e "Current Network Information:"`

echo "Wireless AP:" $myvar1

myen0=`ifconfig en0 | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'`

if [ "$myen0" != "" ]
then
    echo "Ethernet : $myen0"
else
    echo "Ethernet : INACTIVE"
fi

myen1=`ifconfig en1 | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'`

echo "Airport IP : " $myen1

ext1=`curl --silent http://checkip.dyndns.org | awk '{print $6}' | cut -f 1 -d "<"`

echo "External IP : " $ext1
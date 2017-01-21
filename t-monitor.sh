#!/bin/bash
# Furong Peng
#  pengfurong2009@gmail.com


max_t=28  # the max temper.  the default is 37
count=0
max_count=1000  #  check temperature in how many seconds. the default is 1200
base="$(dirname $(readlink -f $0))"
femail="${base}/email.cfg"  # email configuration file
fmessage="${base}/message.txt"

my_sleep() {
  for i in $(seq 1 2 $1)
  do
      sleep 0.1
      if [ ! -f  /var/lock/t-monitor ]; then
           break
      fi
  done
}

while [ -f  /var/lock/t-monitor ] ;do
    # reading temperature, the response is T1=+31.3 \n T2=+33.2
    # while loop to read the temperature line by line
    cat /dev/ttyUSB0 |	\
	while read T; do
	    if [ ! -f  /var/lock/t-monitor ]; then
		break  # the service is set to be stoped
	    fi
	    # remove = and get the integer of temperature
	    array=(${T//=/ })
	    array=${array[1]}
	    array=(${array//./ })
	    # b is the temperature
	    b=${array[0]//+/}
            if [[ ${b} -gt ${max_t} ]]; then
		# Send notification
		if [ $count = 0 ]; then
		    echo "High temperature warrning" > $fmessage
		    echo "temperature is $T now !" >>  $fmessage
		    date >> $fmessage
		    python "$base/Sendmail.py" $femail $fmessage
		fi
		# increasing the count
		count=`expr $count + 1 `
		count=`expr $count % $max_count `
	    fi
	    # wait for 1 second
        done
    my_sleep 10
done

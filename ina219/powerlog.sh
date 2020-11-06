#!/bin/bash

cd /opt/powerlog
LOW=30
MAXVOLT=834
MINVOLT=690
DATE=$(date +"%Y%m%d-%H:%M:%S")
POWER=$(python3 ./powerlog.py short)
VOLTAGE=$(( $(echo ${POWER} | awk -F',' '{print $1}') ))
CURRENT=$(( $(echo ${POWER} | awk -F',' '{print $2}') ))
PERCENT=$(( $(echo ${POWER} | awk -F',' '{print $4}') ))

LOG="/var/log/powerlog.log"

#echo "Voltage: ${VOLTAGE} - ${MINVOLT}" >> ${LOG}
#echo "Current: ${CURRENT}" >> ${LOG}
#echo "Percent: ${PERCENT}" >> ${LOG}

if [[ ( ${PERCENT} -lt ${LOW} && ${CURRENT} -lt 0 ) || ( ${VOLTAGE} -lt ${MINVOLT} ) ]];
then
	echo "${DATE} - ${POWER}" >> ${LOG}
	echo "${DATE} - Powering down." >> ${LOG}
	shutdown -h now
else
	echo "${DATE} - ${POWER}" >> ${LOG}
fi

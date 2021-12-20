#!/bin/bash
if [ "$( systemctl is-active docker)" = "active" ]
then
  echo docker is running
else
  echo "starting docker......"
  systemctl start docker
  systemctl status docker
  docker start $(docker ps -a | grep -v "NAMES" | awk '{ print $NF }'| tr "\n" " " | sort -k 7,9 -h)
fi


if [[ $( docker ps | wc -l) -le 1 ]]
then
  docker start $(docker ps -a | grep -v "NAMES"| grep "azure-agent-headless" | awk '{ print $NF }'| tr "\n" " " | sort -k 7,9 -h)
else
  echo "containers are running."
fi

#!/bin/bash

used=$(findmnt -no use% /mnt | awk '{$1=$1;print}' | cut -c1,2)
#used=$( findmnt -no use% /mnt | cut -f2 -d" " | cut -c1,2 )
DAYOFWEEK=$(date +"%u") # use $(date +"%a") for getting day name like Mon, TUE
image=test:latest

send_mail()
{
    curl --request POST \
  --url https://api.sendgrid.com/v3/mail/send \
  --header "Authorization: Bearer $API" \
  --header 'Content-Type: application/json' \
  --data '{"personalizations": [{"to": [{"email": "test@example.com"}]}],"from": {"email": "ankit@example.com"},"subject": "Infra","content": [{"type": "text/plain", "value": "The docker mount volume is '$used'% occupied."}]}'
}

if [[ $used -gt 75 ]]
then
  if [[ $DAYOFWEEK -eq 6 ]]
  then
    echo "Cleaning automation agents and recreating."
    docker rm -f $(docker ps -a | grep -v "NAMES"| grep "agent" | awk '{ print $NF }'| tr "\n" " " | sort -k 7,9 -h)
    docker login <repo_url> --username <username> --password $TOKEN
    pool="-azure"
    prefix="headless"
    for (( i = 1; i < 17; i++ )); do
      agent_name=${prefix}-${i}
      docker run -d  \
                 -e VSTS_ACCOUNT=<Account-name> \#eg:GP-SP
                 -e VSTS_TOKEN=<PAT> \
                 -e VSTS_AGENT=$agent_name \
                 -e VSTS_POOL=$pool \
                 -e VSTS_WORK='/var/vsts/$VSTS_AGENT' \
                 -e Agent.DisableUpdate=true \
                 -v /var/run/docker.sock:/var/run/docker.sock \
                 -it  --name $agent_name  $image

    done
  fi
  #send_mail
fi

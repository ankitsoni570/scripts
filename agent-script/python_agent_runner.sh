#!/bin/bash -x

image=python-automation-agent

echo "raising new agents"

pool='python-automation'
echo "pool name: $pool"

echo "initial index:"
read -r
index=$REPLY

echo "how many agents to raise:"
read -r
amount=$REPLY

echo "enter the PAT token:"
read -r
token=$REPLY

prefix='python-automation'
echo "agent prefix is: $prefix"

echo "docker secret: "
read -s
echo $REPLY >  password.txt
cat password.txt | docker login <repo-url> --username <username> --password-stdin
rm password.txt

for (( i = $index; i < $index+$amount; i++ )); do
    agent_name=${prefix}-${i}
    docker run -d  \
               -e AZP_URL=https://dev.azure.com/<org> \
               -e AZP_TOKEN=$token \
               -e AZP_AGENT_NAME=$agent_name \
               -e AZP_POOL=$pool \
               -e AZP_WORK='/azp/$AZP_AGENT_NAME' \
               -v /var/run/docker.sock:/var/run/docker.sock \
               -it  --name $agent_name  $image

done

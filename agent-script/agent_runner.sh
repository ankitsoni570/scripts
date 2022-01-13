#!/bin/bash -x

image=agent:latest

echo "raising new agents"
echo "pool name: "
read -r
pool=$REPLY

echo "initial index:"
read -r
index=$REPLY

echo "how many agents to raise:"
read -r
amount=$REPLY

echo "agent prefix:"
read -r
prefix=$REPLY

echo "docker secret: "
read -s
echo $REPLY >  password.txt
cat password.txt | docker login <repo-url> --username <username> --password-stdin
rm password.txt

for (( i = $index; i < $index+$amount; i++ )); do
    agent_name=${prefix}-${i}
    docker run -d  \
               -e VSTS_ACCOUNT=SP \
               -e VSTS_TOKEN=<PAT> \
               -e VSTS_AGENT=$agent_name \
               -e VSTS_POOL=$pool \
               -e VSTS_WORK='/var/vsts/$VSTS_AGENT' \
               -e Agent.DisableUpdate=true \
               -e NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/misys.crt \
               -v /var/run/docker.sock:/var/run/docker.sock \
               -it  --name $agent_name  $image

done


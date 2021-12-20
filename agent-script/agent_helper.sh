#!/bin/bash
while :
do
  echo "I'm here to help with agent"
  echo "Please enter a command to run (use help if needed)"
  read -r


  case $REPLY in
  help)
    echo "disk_prep - prepares a disk for installation"
    echo "install_docker - installs and configures docker"
    echo "run_agents - runs agents"
    echo "quit - exit"
    ;;
  disk_prep)
    . ./agent_disk.sh
    ;;
  install_docker)
    . ./agent_install_docker.sh
    ;;
  run_agents)
    . ./agent_runner.sh
    ;;
  quit)
    break
    ;;
  *)
    echo "wrong command"
    ;;
  esac
done
#!/bin/bash

echo 'Starting to Deploy...'
ssh ec2-user@ip-172-31-47-89 " sudo docker image prune -f
        cd PROG/winecellar/API
        chmode 777 deploy_to_aws.sh
        sudo docker-compose down
        git fetch origin
        git reset --hard origin/develop  &&  echo 'You are doing well'
        sudo docker-compose build && sudo docker-compose up -d
        "
echo 'Deployment completed successfully'

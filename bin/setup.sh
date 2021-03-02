# sudo apt-get install python3-dev \
# pip install -r requirements.txt

#!/bin/bash

if [[ ! -f .env ]];then
    echo "You must create your .env file"
    echo "See docker-compose.yml to check for default values"
    exit 1
fi

source bin/settings.sh

set -e

docker build -t clabs-$PROJECT_NAME -f Dockerfile.local .

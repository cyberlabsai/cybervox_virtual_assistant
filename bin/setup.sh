# sudo apt-get install python3-dev \
#!/bin/bash
RUN="pip3 install $( sed 's/.*/&/' requirements.txt | paste -sd' ' - )" &&
eval $RUN \ 
cp .env.example .env && cp actions.example.json actions.json

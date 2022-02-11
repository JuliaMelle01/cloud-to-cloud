# Application settings
# Path to your python version in pipenv
PYTHON_PIPENV_PATH=/home/pi/.local/share/virtualenvs/cloud-to-cloud-NTmyZdzI/bin/python3

PYTHON_MAIN_FILE_PATH=/home/pi/Documents/codingIxD/cloud-to-cloud/src/main.py

# get data from tshark interface capture
sudo /usr/bin/tshark -T ek | sudo $PYTHON_PIPENV_PATH $PYTHON_MAIN_FILE_PATH


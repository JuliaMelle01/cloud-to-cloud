#!/bin/bash

# Fritzbox settings
# This is the address of the router
FRITZIP=http://fritz.box

# This is the WAN interface
IFACE="2-0"

# Lan Interface
#IFACE="1-lan"

# If you use password-only authentication use 'dslf-config' as username.
FRITZUSER="fritz0242"
FRITZPWD="kippe1358"

SIDFILE="/tmp/fritz.sid"

FRITZBOX_IP_ADDRESS=192.168.178.1

# Application settings
# Path to your python version in pipenv
PYTHON_PIPENV_PATH=/home/pi/.local/share/virtualenvs/cloud-to-cloud-NTmyZdzI/bin/python3

PYTHON_MAIN_FILE_PATH=/home/pi/Documents/codingIxD/cloud-to-cloud/src/main.py

# Start application script
if [ -z "$FRITZPWD" ] || [ -z "$FRITZUSER" ]  ; then echo "Username/Password empty. Usage: $0 <username> <password>" ; exit 1; fi

echo "Trying to login into $FRITZIP as user $FRITZUSER"

if [ ! -f $SIDFILE ]; then
  touch $SIDFILE
fi

SID=$(cat $SIDFILE)

# Request challenge token from Fritz!Box
CHALLENGE=$(curl -k -s $FRITZIP/login_sid.lua |  grep -o "<Challenge>[a-z0-9]\{8\}" | cut -d'>' -f 2)

# Very proprieatry way of AVM: Create a authentication token by hashing challenge token with password
HASH=$(perl -MPOSIX -e '
    use Digest::MD5 "md5_hex";
    my $ch_Pw = "$ARGV[0]-$ARGV[1]";
    $ch_Pw =~ s/(.)/$1 . chr(0)/eg;
    my $md5 = lc(md5_hex($ch_Pw));
    print $md5;
  ' -- "$CHALLENGE" "$FRITZPWD")
  curl -k -s "$FRITZIP/login_sid.lua" -d "response=$CHALLENGE-$HASH" -d 'username='${FRITZUSER} | grep -o "<SID>[a-z0-9]\{16\}" | cut -d'>' -f 2 > $SIDFILE

SID=$(cat $SIDFILE)

# Check for successfull authentification
if [[ $SID =~ ^0+$ ]] ; then echo "Login failed. Did you create & use explicit Fritz!Box users?" ; exit 1 ; fi

echo "Capturing traffic on Fritz!Box interface $IFACE ..." 1>&2

# Capture traffic
ping $FRITZBOX_IP_ADDRESS & wget --no-check-certificate -qO- $FRITZIP/cgi-bin/capture_notimeout?ifaceorminor=$IFACE\&snaplen=\&capture=Start\&sid=$SID | sudo /usr/bin/tshark -i - -T ek | sudo $PYTHON_PIPENV_PATH $PYTHON_MAIN_FILE_PATH

#!/bin/bash

#!/bin/bash
DEVICE="public@192.168.1.1"

MRTGBIN="/home/net484/student/net484s02/mrtg/mrtg-2.17.7/bin"
MRTGHOME=/home/net484/student/net484s02/public_html/mrtg
cd $MRTGHOME
CFGFILE=$MRTGHOME/mrtg.cfg.1
LANG=C
export LANG
if [[ -s $CFGFILE ]]
then
 :
else
 $MRTGBIN/cfgmaker --global "WorkDir: $MRTGHOME" --output $CFGFILE $DEVICE
fi
$MRTGBIN/mrtg $CFGFILE
$MRTGBIN/indexmaker --output=index_192.168.1.1.html $CFGFILE

DEVICE="public@192.168.1.2"

MRTGBIN="/home/net484/student/net484s02/mrtg/mrtg-2.17.7/bin"
MRTGHOME=/home/net484/student/net484s02/public_html/mrtg
cd $MRTGHOME
CFGFILE=$MRTGHOME/mrtg.cfg.2
LANG=C
export LANG
if [[ -s $CFGFILE ]]
then
 :
else
 $MRTGBIN/cfgmaker --global "WorkDir: $MRTGHOME" --output $CFGFILE $DEVICE
fi
$MRTGBIN/mrtg $CFGFILE
$MRTGBIN/indexmaker --output=index_192.168.1.2.html $CFGFILE

DEVICE="public@192.168.1.3"

MRTGBIN="/home/net484/student/net484s02/mrtg/mrtg-2.17.7/bin"
MRTGHOME=/home/net484/student/net484s02/public_html/mrtg
cd $MRTGHOME
CFGFILE=$MRTGHOME/mrtg.cfg.3
LANG=C
export LANG
if [[ -s $CFGFILE ]]
then
 :
else
 $MRTGBIN/cfgmaker --global "WorkDir: $MRTGHOME" --output $CFGFILE $DEVICE
fi
$MRTGBIN/mrtg $CFGFILE
$MRTGBIN/indexmaker --output=index_192.168.1.3.html $CFGFILE
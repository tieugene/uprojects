#/bin/sh
# tool to update 1C repo
# need: wget, curl, dosemu|wine
# TODO:
# 1. create dest dir tree
# 2. Rp's
# 3. logfile


### defines
# dir where all 1C files are
#URLBASE="http://www.1c.ru/buhplace"
#URLAUTH="$URLBASE/auth.asp"
#URLGET="$URLBASE/getfile.asp"
URLBASE="http://downloads.1c.ru"
URLAUTH="$URLBASE/auth.jsp"
URLGET="$URLBASE/get.jsp"
BASEDIR="/mnt/shares/tmp/1C"
TSUBDIR="Tunes"
RSUBDIR="Reports"
# ask its path w/ infodat path
ASKITS="/usr/local/bin/askits /usr/local/share/its/INFO.DAT"
# working directory
TMPDIR="/var/tmp/1C"
# logger
LOGFILE="/var/log/update1c.log"
# packer
PACKER="tar zcf"
PACKEXT="tar.gz"

### main
# 0. prepare
mkdir -p $TMPDIR
BACKPATH=`pwd`
cd $TMPDIR
rm -rf $TMPDIR/*
# 1. generate keys
KEY1=`$ASKITS -v`
KEY2=`curl $URLAUTH?its=$KEY1`
KEY3=`$ASKITS $KEY2`
MAGIC="$URLGET?its=$KEY1&addr=$KEY2&d=$KEY3"
# 2. for each dir in Tunes
for d in $(ls $BASEDIR/$TSUBDIR); do
	#echo $d
	# 2.1. get 1C last ver
	THEYVER=`curl "$URLBASE/ipp/ITSREPV/$d/VER.ID" | tr -d .`
	# 2.2. get my last ver
	MYVER=`ls -1 $BASEDIR/$TSUBDIR/$d | sort | cut -d . -f 1 | colrm 1 1 | tail -n 1`
	echo "They: $THEYVER, My: $MYVER"
	# 2.3. if new...
	if [ -z $MYVER ] || [ $MYVER -lt $THEYVER ] ; then
		# 2.3.1 download update
		#echo "new tune: $d/R$THEYVER"
		#echo "$MAGIC&file=update.exe&dir=$d"
		wget -q "$MAGIC&dir=$d&file=UPDATE.EXE"
		# 2.3.2. unpack them
		if [ -f UPDATE.EXE ] ; then
			dosemu -dumb -quiet UPDATE.EXE
			rm -f UPDATE.EXE
			chmod -R a-x+X *
			$PACKER $BASEDIR/$TSUBDIR/$d/R$THEYVER.$PACKEXT .
			rm -rf *
		fi
	fi
done

# 3. for each dir in Reports
for d in $(ls $BASEDIR/$RSUBDIR); do
	# 3.1. for each YQ in this repo type
	#FRESHVER=`curl $URLBASE/ITSREPV/Reports/$d/Ver.id`
	for YQ in $(ls -1 $BASEDIR/$RSUBDIR/$d | colrm 7 | sort | uniq); do
		MYVER=`basename $(ls -1 $BASEDIR/$RSUBDIR/$d/$YP* | sort | tail -n 1 | cut -d . -f 1) | colrm 1 6`
		#echo "Myver: $MYVER"
		if [ d="GeneralN" ]; then
			REPO="Gen"
		else
			REPO=$d
		fi
		UREPO=`echo "$REPO" | tr [:lower:] [:upper:]`
		UYQ=`echo "$YQ" | tr [:lower:] [:upper:]`
		SRCURL="$MAGIC&dir=/REPORTS/$UREPO/$UYQ.GRP&file"
		VERFILE="VER.ID"
		LSTFILE="LOADLST.TXT"
		#echo "$SRCURL"
		NEWVER=`curl "$SRCURL=$VERFILE" | colrm 1 4`
		#echo "Myver: $MYVER"
		#echo "NewVer: $NEWVER"
		if [ $MYVER -lt $NEWVER ] ; then
			echo "new report: $d/$THEYVER"
			# get filelist
			wget "$SRCURL=$VERFILE"
			wget "$SRCURL=$LSTFILE"
			# get all
			for FILE in `cat $LSTFILE | grep -v ^/ | cut -f 1 -d ";"`; do
				echo "Donloading $FILE..."
				wget -q "$SRCURL=$FILE"
			done
			chmod -R a-x+X *
			tar cf $BASEDIR/$RSUBDIR/$d/$YQ$NEWVER.tar . && rm -rf *
		fi
	done
done

cd $BACKPATH

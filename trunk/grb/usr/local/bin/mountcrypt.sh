#!/bin/sh
# mount crypted partition using keyfile@usbstick & password
# 0. vars
PGLOCK="postgresql"
CRYPTDEV="/dev/sdc2"
DMDEV="cryptfs"
CRYPTMNT="/mnt/cryptfs"
STICKMNT="/mnt/usbstick"
KEYFILE="keyfile.gpg"

# 0. stop postgres
if [ -f /var/lock/subsys/$PGLOCK ] ; then
	service postgresql stop
fi
# 1. check partition already mounted
if [ "`mount -l | gawk '{print $3}' | grep ^$CRYPTMNT$`" != "" ]; then
	echo "ERR: Crypted partition already mounted."
	exit 0
fi
# 2. check usbstick mounted
if [ "`mount -l | gawk '{print $3}' | grep ^$STICKMNT$`" == "" ]; then
	echo "ERR: USB stick not mounted."
	exit 1
fi
# 3. Check keyfile exists
if [ ! -e $STICKMNT/$KEYFILE ]; then
	echo "ERR: Keyfile not exists."
	exit 1
fi
# 4. Try expand key, open luks, mount and start pg
gpg -o - $STICKMNT/$KEYFILE | cryptsetup --key-file - luksOpen $CRYPTDEV $DMDEV && mount /dev/mapper/$DMDEV $CRYPTMNT && service postgresql start

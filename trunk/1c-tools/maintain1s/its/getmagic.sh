#/bin/sh
# tool to get actual magic URL

# ask its path w/ infodat path
ASKITS="/usr/local/bin/askits /usr/local/share/its/INFO.DAT"
# working directory

KEY1=`$ASKITS -v`
KEY2=`curl http://www.1c.ru/buhplace/auth.asp?its=$($ASKITS -v)`
KEY3=`$ASKITS $KEY2`
echo "http://www.1c.ru/buhplace/getfile.asp?its=$KEY1&addr=$KEY2&d=$KEY3&file=...&dir="

#!/bin/sh
#
# Copyright (C) 2008; TI_Eugene, SlavaZ
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer,
#    without modification.
# 2. Redistributions in binary form must reproduce at minimum a disclaimer
#    substantially similar to the "NO WARRANTY" disclaimer below
#    ("Disclaimer") and any redistribution must be conditioned upon
#    including a substantially similar Disclaimer requirement for further
#    binary redistribution.
# 3. Neither the names of the above-listed copyright holders nor the names
#    of any contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# Alternatively, this software may be distributed under the terms of the
# GNU General Public License ("GPL") version 2 as published by the Free
# Software Foundation.
#
# NO WARRANTY
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTIBILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDERS OR CONTRIBUTORS BE LIABLE FOR SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGES.
# 

. ./update1c.conf

[ -z "$MY_CHARSET" ] && MY_CHARSET="UTF-8"
[ -z "$STD_OUT" ] && STD_OUT="/dev/stdout"
[ -z "$STD_ERR" ] && STD_ERR="/dev/stderr"

# ******************************************************************************
# Ниже этого текста не правь - убьёт!!!
# ------------------------------------------------------------------------------
_calcRecode(){
    RECODE=$(echo $LANG| awk -F '.' '{print $2}')
    [ "$RECODE" != "$MY_CHARSET" ] \
	&& echo "iconv -f $MY_CHARSET -t $RECODE" \
	|| echo "cat"
}
# ------------------------------------------------------------------------------
[ -z "$RECODE" ] && {
    export RECODE=$(_calcRecode)
}
# ------------------------------------------------------------------------------
_print(){
    echo "$1" | $RECODE >$2
}
# ------------------------------------------------------------------------------
_echo(){
    _print "$1" "$STD_OUT"
}
# ------------------------------------------------------------------------------
_error(){
    _print "$1" "$STD_ERR"
}
# ------------------------------------------------------------------------------
[ -z "$EXEUNPACKER" ] && {
    which dosemu >/dev/null 2>&1 && {
	EXEUNPACKER="dosemu -t"
    } || {
        which wine >/dev/null 2>&1 && {
	    EXEUNPACKER="wine"
	} || {
	    _error "Эмулятор винды не найден. Установите wine или dosemu"
	    exit 1
	}
    }
}
KEY1=$($ASKITS $INFODAT -v 2>/dev/null) 
[ $? -ne 0 ] && {
    _error "Невозможно получить ключ для скачивания обновлений (1)!"
    exit 1
}
KEY2=$(curl $URLAUTH?its=$KEY1 2>/dev/null)
[ $? -ne 0 ] && {
    _error "Невозможно получить ключ для скачивания обновлений (2)!"
    exit 1
}
KEY3=$($ASKITS $INFODAT $KEY2 2>/dev/null)
[ $? -ne 0 ] && {
    _error "Невозможно получить ключ для скачивания обновлений (3)!"
    exit 1
}
MAGIC="$URLGET?its=$KEY1&addr=$KEY2&d=$KEY3"
# ------------------------------------------------------------------------------
updateTunes(){
 pushd $TMPDIR >/dev/null
 _echo "Получаю $TSUBDIR"
 for d in $(ls $BASEDIR/$TSUBDIR); do
    _echo "	Текущий каталог: $TSUBDIR/$d"
    _echo "	URL дла скачивания: $MAGIC"

    THEYVER=$(curl "$URLBASE/ipp/ITSREPV/$d/VER.ID" 2>/dev/null) 
    [ $? -ne 0 ] && {
	_error "Ошибка получения данных с URL $URLBASE/ipp/ITSREPV/$d/VER.ID"
	# exit 1
	continue
    }
    
    THEYVER=$(echo "$THEYVER" | tr -d .)
    MYVER=$(ls -1 $BASEDIR/$TSUBDIR/$d | sed 's@[^0-9]@@g' | sort -bfr| head -n 1)

    [ -z "$MYVER" ] || [ $MYVER -lt $THEYVER ] && {
        _echo "	Необходимо обновление с версии $MYVER до версии $THEYVER"
        FLNAME="R"$THEYVER".EXE"
	_echo "	Качаем: $MAGIC&dir=$d&file=UPDATE.EXE"
        wget -c -q -O $FLNAME "$MAGIC&dir=$d&file=UPDATE.EXE" 2>/dev/null
        [ $? -ne 0 ] && {
	    _error "	Ошибка получения обновления с URL $MAGIC&dir=$d&file=UPDATE.EXE"
	    # exit 1
	    continue
        }
        _echo "	Обновление скачано в ${TMPDIR}/${FLNAME}"
        mkdir $TMPDIR/unpacked
        pushd $TMPDIR/unpacked >/dev/null
        cp -f ${TMPDIR}/${FLNAME} $TMPDIR/unpacked
    	${EXEUNPACKER} ${TMPDIR}/unpacked/${FLNAME} >/dev/null 2>&1
    	[ $? -ne 0 ] && {
    	    _error "	Ошибка запуска распаковщика!"
    	    rm -fR $TMPDIR/unpacked
    	    continue
    	}
    	rm -f $TMPDIR/unpacked/${FLNAME}
    	[ -z "$(ls . 2>/dev/null)" ] && {
    	    _error "	Распаковщик типо отработал, но ничего из него хорошего не вылезло.."
    	    rm -fR $TMPDIR/unpacked
    	    continue
    	}
    	${PACKER_tunes} $BASEDIR/$TSUBDIR/$d/"R"${THEYVER}.${PACKEXT_tunes} .
    	[ $? -ne 0 ] && {
    	    _error "	Ошибка запуска упаковщика!"
    	    rm -f $BASEDIR/$TSUBDIR/$d/"R"${THEYVER}.${PACKEXT}
    	    continue
    	}
        popd >/dev/null
        rm -fR $TMPDIR/unpacked
    } || {
	_echo "	Обновление не требуется"
    }
 done
 popd >/dev/null
}
# ------------------------------------------------------------------------------
updateReports(){
 pushd $TMPDIR >/dev/null
 _echo "Получаю $RSUBDIR"
 CURR_Y=$(date "+%y")
 #CURR_Q=$(( ($(date "+%m") - 1)/ 3 +1 ))
 CURR_Q="2"
 [ "$TMPDIR" != "/" ] && rm -fR $TMPDIR/*
 for d in $(ls $BASEDIR/$RSUBDIR); do
    [ $d = "GeneralN" ] && REPO="Gen" || REPO=$d
    [ ! -f $BASEDIR/$RSUBDIR/$d/Rp${CURR_Y}q${CURR_Q}* ] && touch $BASEDIR/$RSUBDIR/$d/Rp${CURR_Y}q${CURR_Q}000.tar
    _echo "	Модуль : $REPO"
    for YQ in $(ls -1 $BASEDIR/$RSUBDIR/$d | colrm 7 | sort -u); do
	_FILE=$(basename $(ls -1 $BASEDIR/$RSUBDIR/$d/$YQ* | sort | tail -n 1 | cut -d . -f 1))
	MYVER=$(echo $_FILE | colrm 1 6)
	MY_Q=$(echo $_FILE | sed -r 's@^[Rr][Pp][[:digit:]]*[Qq]([[:digit:]]).*@\1@')
	MY_Y=$(echo $_FILE | sed -r 's@^[Rr][Pp]([[:digit:]]*)[Qq][[:digit:]]*.*@\1@')

	_echo "	Обновляю ${MY_Q}-й квартал ${MY_Y} года..."
	
	UREPO=$(echo "$REPO" | tr [:lower:] [:upper:])
	UYQ=$(echo "$YQ" | tr [:lower:] [:upper:])
	SRCURL="$MAGIC&dir=/REPORTS/$UREPO/$UYQ.GRP&file"
	echo $SRCURL
	VERFILE="VER.ID"
	LSTFILE="LOADLST.TXT"
	#echo "SRCURL: $SRCURL"
	NEWVER=$(curl "$SRCURL=$VERFILE" 2>/dev/null | enconv)
	#echo "New ver: $NEWVER"
	[ $(echo $NEWVER | grep -c '404 Not Found' ) -ne 0 ] && {
	    _error "	нет обновления!"
	    continue
	}
	[ $(echo $NEWVER | grep -c 'Неверный ключ!' ) -ne 0 ] && {
	    _error "	$NEWVER"
	    continue
	}
	NEWVER=$(echo $NEWVER| sed -r 's@.*[Qq][[:digit:]]([[:digit:]]{3}).*$@\1@')
	[ $MYVER -ge $NEWVER ] && {
	    _echo "	нет обновления"
	    continue
	}

	_echo "	Обновление отчёта: $MYVER -> $NEWVER"
	_echo "	Получение списка файлов"
	wget -O $VERFILE "$SRCURL=$VERFILE" >/dev/null 2>&1 || {
	    _error "Ошибка получения $VERFILE!"
	    continue
	}
	wget -O $LSTFILE "$SRCURL=$LSTFILE" >/dev/null 2>&1 ||  {
	    _error "Ошибка получения $LSTFILE!"
	    continue
	}
	_echo "	Список файлов получен. Скачивание по одному"
	for FILE in `cat $LSTFILE | grep -v ^/ | cut -f 1 -d ";"`; do
	    _echo "		Скачивание $FILE..."
	    wget -q -O $FILE "$SRCURL=$FILE" >/dev/null 2>&1
	done
	_echo "	Файлы скачаны. Упаковка..."
	chmod -R a-x+X *
	${PACKER_reports} $BASEDIR/$RSUBDIR/$d/$YQ$NEWVER.${PACKEXT_reports} . && rm -rf *
	_echo "	Файлы упакованы"
    done
 done
 popd >/dev/null
}
# ------------------------------------------------------------------------------

mkdir -p $TMPDIR
[ "$TMPDIR" != "/" ] && rm -fR $TMPDIR/*

updateTunes
updateReports

[ "$TMPDIR" != "/" ] && rm -fR $TMPDIR

exit 0

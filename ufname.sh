#! /bin/bash
# This is  script which takes a list of directories, descends through each one and upper filenames

processfile()
{
        new_name="`echo -n $1 | tr '[:lower:]' '[:upper:]'`"
        if [ "$new_name" != "$1" ] ; then
                while [ -e "$new_name" ] ; do
                        new_name="${new_name}."
                done
                echo changing \"$1\" to \"$new_name\" in `pwd`
                mv -- "$1" "$new_name"
        fi
}

processdir()
{
        set -f
        local savepwd="$PWD"
        if cd "$1" ; then
                set +f
                for file in * ; do
                        set -f
                        if [ "$file" != "." -a "$file" != ".." ] ; then
                                if [ -L "$file" ] ; then
                                        echo "skipping symlink" $file in `pwd`
                                elif [ -d "$file" ] ; then
                                        processdir "$file"
                                elif [ -f "$file" ] ; then
                                        processfile "$file"
                                fi
                        fi
                done
                cd "$savepwd"
        fi
}

shopt -s nullglob dotglob

if [ $# = 0 ] ; then
        echo "$0: must specify a list of directories" >&2
        echo "$0: usage: $0 directory [directory ...]" >&2
        exit 2
fi

while [ $# != 0 ] ; do
        processdir "$1"
        shift
done

exit 0

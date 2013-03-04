#!/bin/sh
# archiving backup copy
tar jcf backup/catmd.$1.tar.bz2 [A-Z]* *dtd *sh src/Makefile src/*.h src/*.cpp
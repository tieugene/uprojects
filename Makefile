# Installation script for highlight.
# See INSTALL for details.
# IMPORTANT: Update highlight.spec file after changing paths!

# Installation directories:

# Destination directory for installation (intended for packagers)
DESTDIR =

# Root directory for final installation
PREFIX = /usr

# Location of the highlight binary:
bin_dir = ${PREFIX}/bin/

# Commands:
INSTALL_PROGRAM=install -Dp -m0755
MKDIR=mkdir -p -m 755
RMDIR=rm -r -f

DEST=unsql
SRC=unsql.cpp
CPP=g++
VER=0.0.3

CFLAGS =  -Wall
LDFLAGS =

$(DEST): $(SRC)
	$(CPP) -o $(DEST) $(CFLAGS) $(LDFLAGS) $(SRC)

all: $(DEST)
	$(CPP) -o $(DEST) $(CFLAGS) $(LDFLAGS) $(SRC)

install: $(DEST)
	install -Dp -m0755 $(DEST) $(DESTDIR)$(bin_dir)$(DEST)

uninstall:
	rm -f $(DESTDIR)$(bin_dir)$(DEST)

clean:
	-rm -f $(DEST)

bz2:
	$(MKDIR) $(DEST)-$(VER)
	cp {$(SRC),Makefile,AUTHORS,COPYING,ChangeLog,README,TODO} $(DEST)-$(VER)
	tar jcf $(DEST)_$(VER).tar.bz2 $(DEST)-$(VER)
	rm -rf $(DEST)-$(VER)

# Target needed for redhat 9.0 rpmbuild
install-strip:

.PHONY: clean all install help uninstall bz2 install-strip

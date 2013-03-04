SRC=faxsplit.cc
DEST=faxsplit
CPP=g++
CFLAGS= -Wall -O3
LDFLAGS= -ltiff
INSDIR=/usr/local/bin

$(DEST): $(SRC)
	$(CPP) -o $(DEST) $(CFLAGS) $(LDFLAGS) $(SRC)

doc:
	a2ps -R --columns=1 -f5 -B -o $(DOC) $(SRC)

install:
	cp $(DEST) $(INSTDIR)

uninstall:
	rm -f $(INSTDIR)/$(DEST)

clean:
	-rm -f *.o *~ *ps $(DEST)

backup:
	tar zcf ../$(DEST).`date +%y%m%d%H%M%S`.tar.gz .

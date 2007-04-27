SRC=rpmtop.cpp
DEST=rpmtop
DOC=rpmtop.ps
CPP=g++
CFLAGS =  -Wall -O3
LDFLAGS = -lrpm

$(DEST): $(SRC)
	$(CPP) -o $(DEST) $(CFLAGS) $(LDFLAGS) $(SRC)

doc:
	a2ps -R --columns=1 -f5 -B -o $(DOC) $(SRC)

install:
	cp $(DEST) /usr/local/bin

uninstall:
	rm -f /usr/local/bin/$(DEST)

clean:
	-rm -f *.o *~ *ps $(DEST)

backup:
	tar zcf ../rpmtop.`date +%y%m%d%H%M%S`.tar.gz .

DEST=mxlview
CPP=g++

CFLAGS =  -Wall 
LDFLAGS = 

.SUFFIXES: .c .cpp
.cpp.o:
	$(CPP) -c $(CFLAGS) $<

OBJS = \
	core.cpp \
	decoder.cpp \
	mxlview.cpp \
	parser.cpp \
	toxml.cpp

$(DEST): $(OBJS)
	$(CPP) -o $(DEST) $(LDFLAGS) $(OBJS)

clean:
	-rm -f *.o *~ $(DEST)
backup:
	tar jcf ../maxlview.`date +%y%m%d%H%M`.tar.bz2 .
DEST=askits
CPP=g++

CFLAGS =  -Wall
LDFLAGS = 

.SUFFIXES: .c .cpp
.cpp.o:
	$(CPP) -c $(CFLAGS) $<

OBJS = askits.o

$(DEST): $(OBJS)
	$(CPP) -o $(DEST) $(LDFLAGS) $(OBJS)

clean:
	-rm -f *.o *~ $(DEST)

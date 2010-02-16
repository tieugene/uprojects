DEST=unsql
CPP=g++

CFLAGS =  -Wall
LDFLAGS = 

.SUFFIXES: .cpp
.cpp.o:
	$(CPP) -c $(CFLAGS) $<

OBJS = unsql.o

$(DEST): $(OBJS)
	$(CPP) -o $(DEST) $(LDFLAGS) $(OBJS)

clean:
	-rm -f *.o *~ $(DEST)

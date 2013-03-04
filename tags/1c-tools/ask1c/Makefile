DEST=ask1c
CPP=c++

CFLAGS =  -Wall `pkg-config glib-2.0 --cflags` `pkg-config libole2-2.0 --cflags`
LDFLAGS = `pkg-config libole2-2.0 --libs` `pkg-config glib-2.0 --libs`

.SUFFIXES: .c .cpp
.cpp.o:
	$(CPP) -c $(CFLAGS) $<

OBJS = \
	ask1c.o \
	mdole.o

$(DEST): $(OBJS)
	$(CPP) -o $(DEST) $(LDFLAGS) $(OBJS)

clean:
	-rm -f *.o *~ $(DEST)

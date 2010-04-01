DEST=catmd
CPP=g++

CFLAGS =  -Wall `pkg-config glib-2.0 --cflags` `pkg-config libole2-2.0 --cflags`
LDFLAGS = -lz `pkg-config libole2-2.0 --libs` `pkg-config glib-2.0 --libs`

.SUFFIXES: .c .cpp
.cpp.o:
	$(CPP) -c $(CFLAGS) $<

OBJS = \
	cc.o \
	commands.o \
	dialog.o \
	dump_data.o \
	expand.o \
	gallery.o \
	guiddata.o \
	main.o \
	menu.o \
	mdole_l.o \
	mms.o \
	mxl.o \
	mxl_in.o \
	mxl_out.o \
	panel.o \
	pic.o \
	prn_data.o \
	rights.o \
	storage.o \
	tree.o \
	ts.o

$(DEST): $(OBJS)
	$(CPP) -o $(DEST) $(LDFLAGS) $(OBJS)

clean:
	-rm -f *.o *~ $(DEST)

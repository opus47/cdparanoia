
###############################################################################
# DO NOT EDIT BELOW! ##########################################################
# (unless, of course, you know what you are doing :) ##########################

VERSION=10.3pre

srcdir=.


FLAGS= -g -O2
OPT=-O2 -fsigned-char $(FLAGS)
DEBUG=-g -Wall -fsigned-char
CC=gcc
LD=gcc
LDFLAGS= $(FLAGS) -ljson-c
AR=ar
RANLIB=ranlib
INSTALL=install
prefix=/usr/local
exec_prefix=${prefix}
BINDIR=${exec_prefix}/bin
MANDIR=${prefix}/share/man
INCLUDEDIR=${prefix}/include
LIBDIR=${exec_prefix}/lib
PKGCONFIGDIR=${exec_prefix}/lib/pkgconfig
PWD = $(shell pwd)

OFILES = main.o report.o header.o buffering_write.o cachetest.o

export STATIC 
export VERSION

ifeq ($(STATIC),TRUE)
	LIBS = interface/libcdda_interface.a paranoia/libcdda_paranoia.a \
		-static -lm -lrt
	LIBDEP = interface/libcdda_interface.a paranoia/libcdda_paranoia.a
else
	LIBS = -lcdda_interface -lcdda_paranoia -lm -lrt
	LIBDEP = interface/libcdda_interface.so paranoia/libcdda_paranoia.so
endif


all: 	
	cd interface && $(MAKE) all
	cd paranoia && $(MAKE) all
	$(MAKE) cdparanoia CFLAGS="$(OPT)" 

debug:  
	cd interface && $(MAKE) debug
	cd paranoia && $(MAKE) debug
	$(MAKE) cdparanoia CFLAGS="$(DEBUG)" STATIC=TRUE

test:	
	cd interface && $(MAKE) all
	cd paranoia && $(MAKE) test

lib:	
	cd interface && $(MAKE) lib
	cd paranoia && $(MAKE) lib

slib:
	cd interface && $(MAKE) slib
	cd paranoia && $(MAKE) slib

install:
	$(INSTALL) -d -m 0755 $(BINDIR)
	$(INSTALL) -m 755 $(srcdir)/cdparanoia $(BINDIR)
	$(INSTALL) -d -m 0755 $(MANDIR)
	$(INSTALL) -d -m 0755 $(MANDIR)/man1
	$(INSTALL) -m 0644 $(srcdir)/cdparanoia.1 $(MANDIR)/man1
	$(INSTALL) -d -m 0755 $(INCLUDEDIR)
	$(INSTALL) -m 0644 $(srcdir)/paranoia/cdda_paranoia.h $(INCLUDEDIR)
	$(INSTALL) -d -m 0755 $(LIBDIR)
	$(INSTALL) -m 0644 $(srcdir)/paranoia/libcdda_paranoia.so.0.$(VERSION) $(LIBDIR)
	$(INSTALL) -m 0644 $(srcdir)/paranoia/libcdda_paranoia.a $(LIBDIR)
	$(INSTALL) -m 0644 $(srcdir)/interface/cdda_interface.h $(INCLUDEDIR)
	$(INSTALL) -m 0644 $(srcdir)/interface/libcdda_interface.so.0.$(VERSION) $(LIBDIR)
	$(INSTALL) -m 0644 $(srcdir)/interface/libcdda_interface.a $(LIBDIR)
	$(INSTALL) -m 0644 $(srcdir)/utils.h $(INCLUDEDIR)
	ln -fs libcdda_interface.so.0.$(VERSION) \
		$(LIBDIR)/libcdda_interface.so.0
	ln -fs libcdda_interface.so.0.$(VERSION) \
		$(LIBDIR)/libcdda_interface.so
	ln -fs libcdda_paranoia.so.0.$(VERSION) \
		$(LIBDIR)/libcdda_paranoia.so.0
	ln -fs libcdda_paranoia.so.0.$(VERSION) \
		$(LIBDIR)/libcdda_paranoia.so
	$(INSTALL) -d -m 0755 $(PKGCONFIGDIR) 
	$(INSTALL) -m 0644 $(srcdir)/cdparanoia-3.pc $(PKGCONFIGDIR) 

cdparanoia:	$(OFILES) $(LIBDEP)
		$(LD) $(CFLAGS) $(LDFLAGS) $(OFILES) \
		-L$(PWD)/paranoia -L$(PWD)/interface \
		-o cdparanoia $(LIBS)

.c.o:
	$(CC) $(CFLAGS) -c $<

clean:
	cd interface && $(MAKE) clean
	cd paranoia && $(MAKE) clean
	-rm -f cdparanoia *~ config.* *.o *.wav *.aifc *.raw \
		verify_test core gmon.out

distclean:
	cd interface && $(MAKE) distclean
	cd paranoia && $(MAKE) distclean
	-rm -f cdparanoia *~ config.* *.o *.wav *.aifc *.raw test.file \
		Makefile verify_test core gmon.out cdparanoia-3.pc

.PHONY: all debug test lib slib install clean distclean

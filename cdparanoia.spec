%define ver	9.8
%define realver	alpha%{ver}

Name: cdparanoia
Version: %{realver}
Release: 22
License: GPL
Group: Applications/Multimedia
Source: http://www.xiph.org/paranoia/download/%{name}-III-%{realver}.src.tgz 
Url: http://www.xiph.org/paranoia/index.html
BuildRoot: %{_tmppath}/cdparanoia-%{version}-root
Requires: cdparanoia-libs = %{version}-%{release}
Obsoletes: cdparanoia-III
Summary: A Compact Disc Digital Audio (CDDA) extraction tool (or ripper).

%description 
Cdparanoia (Paranoia III) reads digital audio directly from a CD, then
writes the data to a file or pipe in WAV, AIFC or raw 16 bit linear
PCM format.  Cdparanoia doesn't contain any extra features (like the ones
included in the cdda2wav sampling utility).  Instead, cdparanoia's strength
lies in its ability to handle a variety of hardware, including inexpensive
drives prone to misalignment, frame jitter and loss of streaming during
atomic reads.  Cdparanoia is also good at reading and repairing data from
damaged CDs.

%package -n cdparanoia-devel
Summary: Development tools for libcdda_paranoia (Paranoia III).
Group: Development/Libraries
Requires: cdparanoia-libs = %{version}-%{release}

%description -n cdparanoia-devel
The cdparanoia-devel package contains the static libraries and header
files needed for developing applications to read CD Digital Audio disks.

%package -n cdparanoia-libs
Summary: Libraries for libcdda_paranoia (Paranoia III).
Group: Development/Libraries

%description -n cdparanoia-libs
The cdparanoia-libs package contains the dynamic libraries needed for
applications which read CD Digital Audio disks.

%prep
%setup -q -n %{name}-III-%{realver}

%build
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
export OPT="${CFLAGS:-%optflags}"
%configure --includedir=%{_includedir}/cdda
make OPT="$OPT"

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}/cdda
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0755 cdparanoia $RPM_BUILD_ROOT%{_bindir}
install -m 0644 cdparanoia.1 $RPM_BUILD_ROOT%{_mandir}/man1/ 
install -m 0644 utils.h paranoia/cdda_paranoia.h interface/cdda_interface.h \
	$RPM_BUILD_ROOT%{_includedir}/cdda
install -m 0755 paranoia/libcdda_paranoia.so.0.%{ver} \
	interface/libcdda_interface.so.0.%{ver} \
	$RPM_BUILD_ROOT%{_libdir}
install -m 0755 paranoia/libcdda_paranoia.a interface/libcdda_interface.a \
	$RPM_BUILD_ROOT%{_libdir}

/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libcdda_paranoia.so.0.%{ver} libcdda_paranoia.so
ln -s libcdda_interface.so.0.%{ver} libcdda_interface.so
popd

%post -n cdparanoia-libs
/sbin/ldconfig

%postun -n cdparanoia-libs
if [ "$1" -ge "1" ]; then
  /sbin/ldconfig
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files -n cdparanoia
%defattr(-,root,root)
%doc README GPL FAQ.txt
%{_bindir}/*
%{_mandir}/man1/*

%files -n cdparanoia-libs
%defattr(-,root,root)
%{_libdir}/*.so*

%files -n cdparanoia-devel
%defattr(-,root,root)
%{_includedir}/cdda
%{_includedir}/cdda/*
%{_libdir}/*.a

%changelog
* Fri Jun 25 2004 Peter Jones <pjones@redhat.com> alpha9.8-22
- take ownership of %{_includedir}/cdda
- sync to mainline

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Peter Jones <pjones@redhat.com> alpha9.8-20
- take ownership of %{_includedir}/cdda

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Peter Jones <pjones@redhat.com> alpha9.8-17
- typo fix (g_fd -> fd)
- add errno output

* Tue May 06 2003 Peter Jones <pjones@redhat.com> alpha9.8-16
- fix warnings on switches
- use O_EXCL

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 25 2002 Tim Powers <timp@redhat.com> alpha9.8-13
- fix %%install references in the changelog so that it will rebuild properly

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> alpha9.8-12
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr  3 2002 Peter Jones <pjones@redhat.com> alpha9.8-8
- don't strip, let rpm do that

* Mon Feb 25 2002 Tim Powers <timp@redhat.com> alpha9.8-7
- fix broken Obsoletes of cdparanoia-devel

* Wed Jan  2 2002 Peter Jones <pjones@redhat.com> alpha9.8-7
- minor cleanups of $RPM_BUILD_ROOT pruning

* Thu Dec  6 2001 Peter Jones <pjones@redhat.com> alpha9.8-6
- move includes to %{_includedir}/cdda/
- add utils.h to %%install
- clean up %%install some.

* Sun Nov  4 2001 Peter Jones <pjones@redhat.com> alpha9.8-5
- make a -libs package which contains the .so files
- make the cdparanoia dependancy towards that, not -devel

* Thu Aug  2 2001 Peter Jones <pjones@redhat.com>
- bump the release not to conflict with on in the RH build tree :/
- reverse devel dependency

* Wed Aug  1 2001 Peter Jones <pjones@redhat.com>
- fix %post and %postun to only run ldconfig for devel packages

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- devel now depends on package

* Wed Mar 28 2001 Peter Jones <pjones@redhat.com>
- 9.8 release.

* Tue Feb 27 2001 Karsten Hopp <karsten@redhat.de>
- fix spelling error in description

* Thu Dec  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- rebuild for new tree

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 06 2000 Preston Brown <pbrown@redhat.com>
- revert name change
- use new rpm macro paths

* Wed Apr 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Switched spec file from the one used in Red Hat Linux 6.2, which
  also changes the name
- gzip man page

* Thu Dec 23 1999 Peter Jones <pjones@redhat.com>
- update package to provide cdparanoia-alpha9.7-2.*.rpm and 
  cdparanoia-devel-alpha9.7-2.*.rpm.  Also, URLs point at xiph.org
  like they should.

* Wed Dec 22 1999 Peter Jones <pjones@redhat.com>
- updated package for alpha9.7, based on input from:
  Monty <xiphmont@xiph.org> 
  David Philippi <david@torangan.saar.de>

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- updated pacakge

* Tue Oct 06 1998 Michael Maher <mike@redhat.com>
- updated package

* Mon Jun 29 1998 Michael Maher <mike@redhat.com>
- built package

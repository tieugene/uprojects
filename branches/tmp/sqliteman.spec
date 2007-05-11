# spec file for package Sqliteman
#
# Copyright (c) 2007 Petr Vanek
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:         sqliteman
URL:          http://www.assembla.com/space/sqliteman
License:      GPL
Group:        Development/Databases
Summary:      Lightweigth but powerfull Sqlite3 manager
Version:      0.99
#Release:      %{builddate}_suse102
Release:      20070509
Source:       %{name}-%{version}-%{release}.tar.gz
Requires:     qt4 >= 4.2.0 qt4-sqlite >= 4.2.0
BuildRequires: qt4-devel >= 4.2.0 qt4-sqlite cmake
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
The best developer's and/or admin's GUI tool for Sqlite3
in the world. No joking here (or just a bit only) - it
contains the most complette feature set of all tools available.

Authors:
--------
	Petr Vanek <petr@scribus.info>

%prep
%setup -q

%build
cmake \
	-DCMAKE_C_FLAGS="%{optflags}" \
	-DCMAKE_CXX_FLAGS="%{optflags}" \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=%{buildroot}/usr \
	%{_builddir}/%{name}-%{version}
%{__make} %{?jobs:-j%jobs}
#	-DCMAKE_INSTALL_PREFIX=%{_prefix} \

%install
%makeinstall

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}
%{_datadir}
#%{_libdir}/wengophone/libowwebcam.so
#%{_datadir}/wengophone
#%{_datadir}/applications/wengophone.desktop
#%{_datadir}/pixmaps/wengophone2.png


%changelog -n sqliteman
* Fri Apr 11 2007 - Eugene Pivnev <ti.eugene@gmail.com>
- initial build for FC6

* Wed Feb 20 2007 - Petr Vanek <petr@scribus.info>
- initial package
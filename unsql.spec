Summary:	1C 7.7 SQL handling utility
Name:		unsql
Version:	0.0.3
Release:	0
Group:		Utility
License:	GPL
Packager:	TI_Eugene <ti.eugene@gmail.com>
Source:		%{name}_%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gcc-c++, glibc-devel
Prefix:		/usr

%description
Utility to decode 1Cv7.DBA file and to set new values in it from CLI.

%prep
%setup

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{makeinstall} DESTDIR=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/%{name}

%changelog
* Sat Jun 5 2010 TI_Eugene <ti.eugene@gmail.com>
- Initial build for openSUSE Build Service

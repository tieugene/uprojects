%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define 	app	run1s

Name:		%{app}-server
Version:	0.0.1
Release:	1
License:	GPL
Group:		Development/Languages
Summary:	Run1s - server side.
URL:		http://code.google.com/p/uprojects/wiki/run1c
Source:		%{name}-%{version}.tar.gz
BuildRequires:	python-devel
Requires:	httpd, python-webpy
BuildArch:	noarch
Prefix:		/usr
BuildRoot:	%{_tmppath}/%{name}-%{version}-build


%description
Run1s-server is server side of Run1s system - to centralize maintaining of 1C databases.
Install and goto http://<host>/run1s/ URL.


%prep
%setup -q


%build


%install
rm -rf %{buildroot}
%{__install} -d %{buildroot}%{_datadir}
%{__cp} -R %{app} %{buildroot}%{_datadir}
%{__install} -D -m 644 %{app}.conf %{buildroot}/etc/httpd/conf.d/%{app}.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO db.dia
/etc/httpd/conf.d/%{app}.conf
%{_datadir}/%{app}


%changelog

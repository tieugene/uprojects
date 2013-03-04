%define VERSION 0.8
# Initial spec file created by autospec ver. 0.8 with rpm 3 compatibility
Summary: rpmorphan list the orphaned rpm packages.
# The Summary: line should be expanded to about here -----^
Summary(fr): rpmorphan liste les packages rpm orphelins.
Name: rpmorphan
Version: %{VERSION}
Release: 1
Group: Applications/System
#Group(fr): (translated group goes here)
License: GPL
Source: rpmorphan-%{VERSION}.tar.gz
BuildRoot: %{_tmppath}/%{name}-root
# Following are optional fields
URL: http://rpmorphan.sourceforge.net
#Distribution: Red Hat Contrib-Net
#Patch: src-%{version}.patch
#Prefix: /usr
BuildArch: noarch
Requires: perl
Requires: rpm
#Obsoletes: 
#BuildRequires: 

%description
rpmorphan  finds  "orphaned"  packages  on  your system. It determines
which packages have no other packages depending on their installation,
and shows you a list of these packages.
It intends to be clone of deborphan debian tools for rpm packages.

It will try to help you to remove unused packages, for exemple :
- after a distribution upgrade
- when you want to suppress packages after some tests

%description -l fr
Le  logiciel  rpmorphan  liste  les  packages  rpm  qui  n'ont plus de
dépendances avec les autres paquets installés sur votre système.
C'est un clone du logiciel deborphan de debian pour les packages rpm.

Il peut vous aider pour supprimer les packages inutilisés, par exemple :
- après une montée de version système
- lors de la suppression de logiciels après des tests

%prep
%setup
#%patch

%build
#echo "build"
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%dir %{_bindir}
%{_bindir}/rpmorphan.pl
%{_bindir}/rpmorphan
%{_bindir}/rpmusage.pl
%{_bindir}/rpmusage
%dir /var/lib/rpmorphan
/var/lib/rpmorphan/keep
%dir %{_mandir}/man1
%doc %{_mandir}/man1/rpmorphan.1*
%doc %{_mandir}/man1/rpmusage.1*
%doc rpmorphan.lsm
%doc Authors
%doc COPYING
%doc Changelog
%doc NEWS
%doc Todo
%doc Makefile
%doc Readme
%doc test_rpmorphan.pl

%changelog
* Tue Mar 06 2007 <gerbier@users.sourceforge.net> 0.8
- add simple graphical user iinterface (optionnal)
- remove global variable opt_verbose
- split code in functions : access_time_filter, read_rpm_data, search_orphans
* Tue Feb 28 2007  <gerbier@users.sourceforge.net> 0.4
- add optionnal cache
* Tue Feb 03 2007  <gerbier@users.sourceforge.net> 0.3
- add rpmusage tool
- add a link from rpmorphan.pl to rpmorphan
* Tue Jan 30 2007  <gerbier@users.sourceforge.net> 0.2
- add permanent exclude list
* Tue Jan 23 2007  <gerbier@users.sourceforge.net> 0.1
- Initial spec file 

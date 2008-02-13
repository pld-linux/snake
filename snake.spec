Summary:	Smart Network Automated Kickstart Environment
Name:		snake
Version:	0.10
Release:	0.6
License:	GPL v2+
Group:		Applications/Networking
URL:		http://hosted.fedoraproject.org/projects/snake/
Source0:	https://fedorahosted.org/snake/attachment/wiki/SnakeReleases/%{name}-%{version}.tar.bz2
# Source0-md5:	2978fb3a5328a268b51703172523f2f7
BuildRequires:	python-devel
BuildRequires:	python-setuptools-devel
Requires:	yum
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
snake is a toolkit for doing automated kickstart-based installations.

%package server
Summary:	Smart Network Automated Kickstart Environment Server
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires:	/sbin/chkconfig
Requires:	logrotate >= 3.5.2
Requires:	mkinitrd
Requires:	pykickstart >= 1.1

%description server
snake-server provides utilities for serving installation trees and
kickstart templates to snake-client systems

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/snake
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/snake/{kickstarts,trees}

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add snake-server

%preun server
if [ "$1" -eq 0 ]; then
	%service snake-server stop
	/sbin/chkconfig --del snake-server
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/snake-install
%attr(755,root,root) %{_sbindir}/snake-install-tui
%attr(755,root,root) %{_sbindir}/snake-tree
%attr(755,root,root) %{_sbindir}/snake-ks
%attr(755,root,root) %{_bindir}/snake-rawhide-status
%dir %{py_sitedir}/snake
%{py_sitedir}/snake/__init__.py[co]
%{py_sitedir}/snake/client.py[co]
%{py_sitedir}/snake/constants.py[co]
%{py_sitedir}/snake/dbushelper.py[co]
%{py_sitedir}/snake/install.py[co]
%{py_sitedir}/snake/log.py[co]
%{py_sitedir}/snake/machineinfo.py[co]
%{py_sitedir}/snake/saverestore.py[co]
%{py_sitedir}/snake/tui.py[co]
%{py_sitedir}/snake/tree.py[co]
%{py_sitedir}/snake/uri.py[co]
%{py_sitedir}/snake/util.py[co]
%{py_sitedir}/snake/xmlhelper.py[co]
%{py_sitedir}/snake/zeroconf.py[co]
%{py_sitedir}/snake-%{version}-*.egg-info
%{_mandir}/man1/snake-tree.1*
%{_mandir}/man1/snake-ks.1*
%{_mandir}/man1/snake-install.1*

%files server
%defattr(644,root,root,755)
%doc docs/DESIGN
%attr(755,root,root) %{_sbindir}/snake-server
%dir %{_localstatedir}/lib/snake
%dir %{_localstatedir}/lib/snake/kickstarts
%{_localstatedir}/lib/snake/kickstarts/minimal.ks
%dir %{_localstatedir}/lib/snake/trees
%config(noreplace) %{_sysconfdir}/snake.conf
%config(noreplace) /etc/logrotate.d/snake-server
%attr(754,root,root) /etc/rc.d/init.d/snake-server
%{py_sitedir}/snake/compose.py[co]
%{py_sitedir}/snake/config.py[co]
%{py_sitedir}/snake/dbushelper.py[co]
%{py_sitedir}/snake/kickstart.py[co]
%{py_sitedir}/snake/labindex.py[co]
%{py_sitedir}/snake/labquery.py[co]
%{py_sitedir}/snake/machine.py[co]
%{py_sitedir}/snake/plugins.py[co]
%{py_sitedir}/snake/server.py[co]
%{py_sitedir}/snake/ksdb.py[co]
%{py_sitedir}/snake/treedb.py[co]

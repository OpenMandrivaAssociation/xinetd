Summary:	Powerful replacement for inetd
Name:		xinetd
Version:	2.3.15
Release:	4
Group:		System/Base
License:	BSD
URL:		http://www.xinetd.org
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
Patch0:		xinetd-2.3.15-tirpc.patch
Source1:	xinetd.init
Source2:	xinetd.default.config
Source3:	convert.pl
Source4:	xinetd-ttime
Source5:	xinetd-utime
Source6:	xinetd-tdtime
Source7:	xinetd-udtime
Source8:	xinetd-echo
Source9:	xinetd-uecho
Source10:	xinetd-chargen
Source11:	xinetd-uchargen
Source12:	xinetd.sysconf
Source13:	xinetd-servers
Source14:	xinetd-services
Source15:	xinetd-xadmin
Source50:	faq.html
Source100:	%name.rpmlintrc
Requires:	tcp_wrappers
Requires(post):	rpm-helper
Requires(postun):	rpm-helper
Requires(preun):	rpm-helper
BuildRequires:	tcp_wrappers-devel
BuildRequires:	tirpc-devel
Obsoletes:	xinetd-ipv6 < %{version}-%{release}
Obsoletes:	xinetd-devel < %{version}-%{release}
Obsoletes:	netkit-base < %{version}-%{release}
Provides:	xinetd-devel
Provides:	netkit-base

%description
xinetd is a powerful replacement for inetd.
xinetd has access control machanisms, extensive logging capabilities,
the ability to make services available based on time, and can place
limits on the number of servers that can be started, among other things.

xinetd has the ability to redirect TCP streams to a remote host and
port. This is useful for those of that use ip masquerading, or NAT,
and want to be able to reach your internal hosts.

xinetd also has the ability to bind specific services to specific
interfaces. This is useful when you want to make services available
for your internal network, but not the rest of the world.  Or to have
a different service running on the same port, but different interfaces.

%package simple-services
Summary:	Internal xinetd simple services
Group:		System/Base
License:	BSD
Requires:	xinetd

%description simple-services
Internal xinetd simple services (not very useful one):

- chargen

Chargen is short for Character Generator and is a service that generates
random characters either in one UDP packet containing a random number (between
0 and 512) of characters, or a TCP session. The UDP Chargen server looks for a
UDP packet on port 19 and responds with the random character packet.

With TCP Chargen, the server sends as a continuous stream of TCP packets once
a connection is made, and until the session closes. The data is thrown away.
Chargen is used to find the cause for dropped packets. It uses TCP/UDP port
19. An infiltrator can create a DoS attack by spoofing an IP address and
causing two devices to send random traffic to each other.

RFC 864 describes the Chargen service.

- daytime

The Daytime protocol is another testing tool and uses port 13 for both UDP and
TCP versions. On receipt of a datagram to port 13, the server in the UDP
version, sends the current date and time in ASCII format in a datagram. The
TCP version, on receipt of a datagram to port 13, and once the connection is
established, sends the date and time in ASCII format and closes the
connection.

RFC 867 describes the Daytime service.

- echo

Echo uses UDP and TCP port 7 and is used as a debgging tool to send any
datagrams received from a source, back to that source. The risk with this is
that someone who has access to the network can overload devices via the Echo
service amounting to a DoS attack.

RFC 862 describes the Echo service.

- time

- servers

Show servers running

- services

Show available services

- xadmin

Show servers running and available services

%prep
%setup -q
%apply_patches
install -m 0644 %SOURCE50 FAQ.html
#chmod a+r INSTALL README FAQ.html CHANGELOG COPYRIGHT xinetd/sample.conf

%build
%serverbuild
%configure2_5x  --with-libwrap --with-inet6
%make

%install
%makeinstall \
    DAEMONDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}/%{_mandir} \
    FMODE="-m 644"

install -m 755 %SOURCE3 %{buildroot}%{_sbindir}/inetdconvert

install -d -m 755 %buildroot%{_sysconfdir}
install -m 644 %SOURCE2 %{buildroot}%{_sysconfdir}/xinetd.conf

install -d -m 755 %buildroot%{_initrddir}/
install -m 755 %SOURCE1 %buildroot%{_initrddir}/xinetd

install -d -m 755 %{buildroot}%{_sysconfdir}/xinetd.d
install -m 644 %SOURCE4 %{buildroot}%{_sysconfdir}/xinetd.d/time
install -m 644 %SOURCE5 %{buildroot}%{_sysconfdir}/xinetd.d/time-udp
install -m 644 %SOURCE6 %{buildroot}%{_sysconfdir}/xinetd.d/daytime
install -m 644 %SOURCE7 %{buildroot}%{_sysconfdir}/xinetd.d/daytime-udp
install -m 644 %SOURCE8 %{buildroot}%{_sysconfdir}/xinetd.d/echo
install -m 644 %SOURCE9 %{buildroot}%{_sysconfdir}/xinetd.d/echo-udp
install -m 644 %SOURCE10 %{buildroot}%{_sysconfdir}/xinetd.d/chargen
install -m 644 %SOURCE11 %{buildroot}%{_sysconfdir}/xinetd.d/chargen-udp
install -m 644 %SOURCE14 %{buildroot}%{_sysconfdir}/xinetd.d/services

install -d -m 755 %buildroot%{_sysconfdir}/sysconfig
install -m 644 %SOURCE12 %{buildroot}%{_sysconfdir}/sysconfig/xinetd

# no need to ship this one since we provide inetdconvert
rm -f %{buildroot}%{_sbindir}/itox
rm -f %{buildroot}%{_sbindir}/xconv.pl
rm -f %{buildroot}/%{_mandir}/man8/itox*

%post
%_post_service %{name}

%preun
%_preun_service  %{name}

%files
%doc INSTALL README FAQ.html CHANGELOG COPYRIGHT xinetd/sample.conf
%config(noreplace) %{_sysconfdir}/sysconfig/xinetd
%config(noreplace) %{_sysconfdir}/xinetd.conf
%{_initrddir}/xinetd
%dir %{_sysconfdir}/xinetd.d
%{_sbindir}/xinetd
%{_sbindir}/inetdconvert
%{_mandir}/*/*

%files simple-services
%config(noreplace) %{_sysconfdir}/xinetd.d/*


%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-13mdv2011.0
+ Revision: 671323
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-12mdv2011.0
+ Revision: 608212
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-11mdv2010.1
+ Revision: 524446
- rebuilt for 2010.1

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.14-10mdv2009.1
+ Revision: 319107
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 2.3.14-9mdv2009.0
+ Revision: 226045
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.3.14-8mdv2008.1
+ Revision: 171187
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Thu Jan 31 2008 Marcelo Ricardo Leitner <mrl@mandriva.com> 2.3.14-7mdv2008.1
+ Revision: 160874
- Fix initscript so that it returns the proper value on status action.

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jun 28 2007 Andreas Hasenack <andreas@mandriva.com> 2.3.14-6mdv2008.0
+ Revision: 45529
- use serverbuild macro


* Mon Mar 05 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.14-5mdv2007.0
+ Revision: 133367
- obsoletes xinetd-ipv6

* Tue Feb 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.3.14-4mdv2007.1
+ Revision: 126594
- init script harmonization with other packages
- large installation sequence cleanup
  don't ship library man pages, as the library is not shipped itself
  init script is not configuration
- drop ugly dual binary setup, and only ship one unique xinetd version
- spec cleanup

  + Andreas Hasenack <andreas@mandriva.com>
    - bump release
    - use C locale instead of en_US, so we don't have to require
      locales-en to be installed (#19106 and #26202)
    - bunzipped some files
    - Import xinetd

* Wed Sep 13 2006 Andreas Hasenack <andreas@mandriva.com> 2.3.14-2mdv2007.0
- don't ignore return values in the init script

* Tue Jan 31 2006 Warly <warly@mandriva.com> 2.3.14-1mdk
- new version

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 2.3.13-7mdk
- fix typo in initscripts

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 2.3.13-6mdk
- convert parallel init to LSB
- fix pre/post requires

* Mon Jan 02 2006 Oden Eriksson <oeriksson@mandriva.com> 2.3.13-5mdk
- fix deps

* Sun Jan 01 2006 Couriousous <couriousous@mandriva.org> 2.3.13-4mdk
- Add parallel init stuff

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 2.3.13-3mdk
- Rebuild

* Sun Jul 31 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.3.13-2mdk
- Fix Build with gcc4 ( Fedora )


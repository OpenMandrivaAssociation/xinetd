Summary:	Powerful replacement for inetd
Name:		xinetd
Version:	2.3.15
Release:	14
Group:		System/Base
License:	BSD
URL:		http://www.xinetd.org
Source0:	http://www.xinetd.org/%{name}-%{version}.tar.gz
Patch0:		xinetd-2.3.15-tirpc.patch
Patch1:		xinetd-2.3.15-CVE-2013-4342.patch
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
Source100:	%{name}.rpmlintrc
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
install -m 0644 %{SOURCE50} FAQ.html
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

install -m 755 %{SOURCE3} %{buildroot}%{_sbindir}/inetdconvert

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/xinetd.conf

install -d -m 755 %{buildroot}%{_initrddir}/
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/xinetd

install -d -m 755 %{buildroot}%{_sysconfdir}/xinetd.d
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xinetd.d/time
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/xinetd.d/time-udp
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/xinetd.d/daytime
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/xinetd.d/daytime-udp
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/xinetd.d/echo
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/xinetd.d/echo-udp
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/xinetd.d/chargen
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/xinetd.d/chargen-udp
install -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/xinetd.d/services

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/sysconfig/xinetd

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

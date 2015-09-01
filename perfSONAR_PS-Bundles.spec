%define relnum 0.8.rc2 
%define disttag pS

Version:        3.5
Name:           perfSONAR-Bundles
Summary:        Bundles of the perfSONAR Software
Release:        %{relnum}.%{disttag}
License:        Distributable, see LICENSE
Group:          Applications/Communications
URL:            http://psps.perfsonar.net/
BuildArch:      noarch

%description
Various bundles of the perfSONAR Software

%package common
Summary:        Package common to all perfSONAR tools
Group:          Applications/Communications
Requires: coreutils
Requires(pre): coreutils
Requires(post): coreutils

%description common
Package common to all perfsonar tools. Creates users, groups, logging directories, etc.

%package Tools
Summary:        pS-Performance Toolkit Bundle - perfSONAR Tools
Group:          Applications/Communications
Requires:       perfSONAR-Bundles-common
Requires:       Internet2-repo
Requires:       bwctl-client
Requires:       bwctl-server
Requires:       ndt-client
Requires:       owamp-client
Requires:       owamp-server
Requires:       nuttcp
Requires:       iperf
Requires:       iperf3
Requires:       traceroute
Requires:       iputils
Requires:       paris-traceroute
Requires:       ntp

%description Tools
The perfSONAR Toolkit - perfSONAR tools bundle

%package TestPoint
Summary:        pS-Performance Toolkit Bundle - minimal test end point
Group:          Applications/Communications
Requires:       Internet2-repo
Requires:       perfSONAR-Bundles-Tools
Requires:       perl-perfSONAR-OPPD-MP-BWCTL
Requires:       perl-perfSONAR-OPPD-MP-OWAMP
Requires:       perl-perfSONAR_PS-LSRegistrationDaemon
Requires:       perl-perfSONAR_PS-RegularTesting
Requires:       perl-perfSONAR_PS-Toolkit-Install-Scripts
Requires:       perl-perfSONAR_PS-MeshConfig-Agent

%description TestPoint
The perfSONAR Toolkit - minimal test point bundle

%package Core
Summary:                pS-Performance Toolkit Core - regular testing and MA
Group:                  Applications/Communications
Requires:               Internet2-repo
Requires:               perfSONAR-Bundles-TestPoint
Requires:               esmond
Requires:               perl-perfSONAR_PS-Toolkit-Install-Scripts

%description Core
The perfSONAR Toolkit - regular testing and MA bundle

%package Complete
Summary:                pS-Performance Toolkit Complete - All perfSONAR Toolkit rpms
Group:                  Applications/Communications
Requires:               Internet2-repo
Requires:               perfSONAR-Bundles-Core
Requires:               perl-perfSONAR_PS-Toolkit
Requires:               perl-perfSONAR_PS-Toolkit-SystemEnvironment

%description Complete
The perfSONAR Toolkit - All perfSONAR Toolkit rpms

%package CentralManagement
Summary:        pS-Performance Toolkit Bundle - Central Management
Group:          Applications/Communications
Requires:       Internet2-repo
Requires:       perl-perfSONAR_PS-MeshConfig-JSONBuilder
Requires:       perl-perfSONAR_PS-MeshConfig-GUIAgent
Requires:       maddash
Requires:       esmond

%description CentralManagement
The perfSONAR Toolkit - Central Management

%pre common
/usr/sbin/groupadd perfsonar 2> /dev/null || :
/usr/sbin/useradd -g perfsonar -r -s /sbin/nologin -c "perfSONAR User" -d /tmp perfsonar 2> /dev/null || :

%post common
mkdir -p /var/log/perfsonar
chown perfsonar:perfsonar /var/log/perfsonar
mkdir -p /var/lib/perfsonar/bundles

#remove this after 3.5rc. Cleans out old method of setting type and version
grep -v "bundle" /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf > /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
mv /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf


%post TestPoint
echo "test-point" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version

%post Core
echo "perfsonar-core" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version

%post Complete
echo "perfsonar-complete" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version

%files
%defattr(0644,perfsonar,perfsonar,0755)

%files Tools
%defattr(0644,perfsonar,perfsonar,0755)

%files TestPoint
%defattr(0644,perfsonar,perfsonar,0755)

%files Core
%defattr(0644,perfsonar,perfsonar,0755)

%files Complete
%defattr(0644,perfsonar,perfsonar,0755)

%files CentralManagement
%defattr(0644,perfsonar,perfsonar,0755)

%files common
%defattr(0644,perfsonar,perfsonar,0755)

%changelog
* Mon Jul 14 2015 andy@es.net
- common bundle
* Mon Jul 06 2015 adelvaux@man.poznan.pl
- Tools bundle
* Wed Mar 25 2015 sowmya@es.net
- Core bundle
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle

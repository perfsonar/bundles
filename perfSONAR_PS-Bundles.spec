%define relnum 0.5.rc1 
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

%package Tools
Summary:        pS-Performance Toolkit Bundle - perfSONAR Tools
Group:          Applications/Communications
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
Requires:       perl-perfSONAR_PS-MeshConfig-Agent
Requires:       maddash
Requires:       esmond

%description CentralManagement
The perfSONAR Toolkit - Central Management

%pre Tools
/usr/sbin/groupadd perfsonar 2> /dev/null || :
/usr/sbin/useradd -g perfsonar -r -s /sbin/nologin -c "perfSONAR User" -d /tmp perfsonar 2> /dev/null || :

%post TestPoint
grep -v "bundle" /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf > /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_type  test-point" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_version  %{version}" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
mv /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf

%post Core
grep -v "bundle" /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf > /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_type  perfsonar-core" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_version  %{version}" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
mv /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf

%post Complete
grep -v "bundle" /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf > /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_type  perfsonar-complete" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
echo "bundle_version  %{version}" >> /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp
mv /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf.tmp /opt/perfsonar_ps/ls_registration_daemon/etc/ls_registration_daemon.conf

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

%changelog
* Mon Jul 06 2015 adelvaux@man.poznan.pl
- Tools bundle
* Wed Mar 25 2015 sowmya@es.net
- Core bundle
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle

%define relnum 0.1.rc1 

Version:        3.5.1
Name:           perfsonar
Summary:        Bundles of the perfSONAR Software
Release:        %{relnum}
License:        Distributable, see LICENSE
Group:          Applications/Communications
URL:            http://www.perfsonar.net/
BuildArch:      noarch

%description
Various bundles of the perfSONAR Software

%package common
Summary:        Package common to all perfSONAR tools
Group:          Applications/Communications
Requires:       coreutils
Requires(pre):  coreutils
Requires(post): coreutils
Obsoletes:      perfSONAR-Bundles-common
Provides:       perfSONAR-Bundles-common

%description common
Package common to all perfsonar tools. Creates users, groups, logging directories, etc.

%package tools
Summary:        perfSONAR active measurement tools
Group:          Applications/Communications
Requires:       perfsonar-common
Requires:       bwctl-client    >= 1.6.0
Requires:       bwctl-server    >= 1.6.0
Requires:       ndt-client
Requires:       owamp-client    >= 3.5.0
Requires:       owamp-server    >= 3.5.0
Requires:       nuttcp
Requires:       iperf
Requires:       iperf3
Requires:       traceroute
Requires:       iputils
Requires:       paris-traceroute
Requires:       ntp
Obsoletes:      perfSONAR-Bundles-Tools
Provides:       perfSONAR-Bundles-Tools

%description tools
The basic command-line measurement tools used by perfSONAR for on-demand tests. 

%package testpoint
Summary:        perfSONAR scheduled testing tools
Group:          Applications/Communications
Requires:       libperfsonar-regulartesting-perl
Requires:       libperfsonar-toolkit-perl 
Requires:       libperfsonar-perl 
Requires:       perfsonar-tools
Requires:       perfsonar-oppd-bwctl
Requires:       perfsonar-oppd-owamp
Requires:       perfsonar-lsregistrationdaemon
Requires:       perfsonar-regulartesting
Requires:       perfsonar-toolkit-install
Requires:       perfsonar-meshconfig-agent
Obsoletes:      perfSONAR-Bundles-TestPoint
Provides:       perfSONAR-Bundles-TestPoint

%description testpoint
Perform regularly scheduled perfSONAR measurements and store the results remotely.

%package core
Summary:                perfSONAR scheduled testing and storage tools
Group:                  Applications/Communications
Requires:               perfsonar-testpoint
Requires:               esmond >= 2.0
Requires:               perfsonar-toolkit-install
Obsoletes:              perfSONAR-Bundles-Core
Provides:               perfSONAR-Bundles-Core

%description core
Perform regularly scheduled perfSONAR measurements and store the results locally.

%package centralmanagement
Summary:        Centrally manage perfSONAR nodes
Group:          Applications/Communications
Requires:       libperfsonar-esmond-perl
Requires:       libperfsonar-sls-perl
Requires:       libperfsonar-toolkit-perl 
Requires:       libperfsonar-perl 
Requires:       perfsonar-meshconfig-jsonbuilder
Requires:       perfsonar-meshconfig-guiagent
Requires:       maddash
Requires:       esmond >= 2.0
Obsoletes:      perfSONAR-Bundles-CentralManagement
Provides:       perfSONAR-Bundles-CentralManagement

%description centralmanagement
Manage, store and visualize results from multiple nodes running perfSONAR measurements. 

%pre common
/usr/sbin/groupadd perfsonar 2> /dev/null || :
/usr/sbin/useradd -g perfsonar -r -s /sbin/nologin -c "perfSONAR User" -d /tmp perfsonar 2> /dev/null || :

%post common
mkdir -p /var/log/perfsonar
chown perfsonar:perfsonar /var/log/perfsonar
mkdir -p /var/lib/perfsonar/bundles

%post testpoint
echo "test-point" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version

%post core
echo "perfsonar-core" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version

%files
%defattr(0644,perfsonar,perfsonar,0755)

%files tools
%defattr(0644,perfsonar,perfsonar,0755)

%files testpoint
%defattr(0644,perfsonar,perfsonar,0755)

%files core
%defattr(0644,perfsonar,perfsonar,0755)

%files centralmanagement
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

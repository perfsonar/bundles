%define perfsonar_auto_version 4.3.0
%define perfsonar_auto_relnum 0.b1.1
%define toolkit_config_base /etc/perfsonar/toolkit/default_service_configs

Version:        %{perfsonar_auto_version}
Name:           perfsonar
Summary:        Bundles of the perfSONAR Software
Release:        %{perfsonar_auto_relnum}%{?dist}
License:        ASL 2.0
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
Requires:       pscheduler-core
Requires:       owamp-client    >= 3.5.0
Requires:       owamp-server    >= 3.5.0
Requires:       twamp-client
Requires:       twamp-server
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
Requires:       libperfsonar-pscheduler-perl
Requires:       libperfsonar-toolkit-perl 
Requires:       libperfsonar-perl 
Requires:       httpd-wsgi-socket
Requires:       perfsonar-tools
Requires:       perfsonar-lsregistrationdaemon
Requires:       perfsonar-toolkit-install
Requires:       perfsonar-psconfig-pscheduler
Requires:       pscheduler-bundle-full
Requires(post): perfsonar-toolkit-install
Obsoletes:      perfSONAR-Bundles-TestPoint
Provides:       perfSONAR-Bundles-TestPoint

%description testpoint
Perform regularly scheduled perfSONAR measurements and store the results remotely.

%package core
Summary:                perfSONAR scheduled testing and storage tools
Group:                  Applications/Communications
Requires:               perfsonar-testpoint
Requires:               perfsonar-toolkit-esmond-utils
Requires:               esmond >= 2.1
Requires:               perfsonar-toolkit-install
Requires(post):         perfsonar-toolkit-esmond-utils
Obsoletes:              perfSONAR-Bundles-Core
Provides:               perfSONAR-Bundles-Core

%description core
Perform regularly scheduled perfSONAR measurements and store the results locally.

%package centralmanagement
Summary:        Centrally manage perfSONAR nodes
Group:          Applications/Communications
Requires:       libperfsonar-esmond-perl
Requires:       libperfsonar-sls-perl
Requires:       libperfsonar-perl 
Requires:       perfsonar-lsregistrationdaemon
Requires:       perfsonar-psconfig-maddash
Requires:       perfsonar-psconfig-publisher
Requires:       perfsonar-toolkit-esmond-utils
Requires:       maddash
Requires:       esmond >= 2.1
Obsoletes:      perfSONAR-Bundles-CentralManagement
Provides:       perfSONAR-Bundles-CentralManagement

%description centralmanagement
Manage, store and visualize results from multiple nodes running perfSONAR measurements. 

%package bwctl-compat
Summary:                perfSONAR BWCTL backward compatibility package
Group:                  Applications/Communications
Requires:               bwctl
Requires:               pscheduler-tool-bwctliperf2
Requires:               pscheduler-tool-bwctliperf3
Requires:               pscheduler-tool-bwctlping
Requires:               pscheduler-tool-bwctltracepath
Requires:               pscheduler-tool-bwctltraceroute

%description bwctl-compat
Installs bwctl/client server and related pScheduler plug-ins for backward compatibility 
with pre-4.0 hosts or those that block the pScheduler port. 

%pre common
/usr/sbin/groupadd -r perfsonar 2> /dev/null || :
/usr/sbin/useradd -g perfsonar -r -s /sbin/nologin -c "perfSONAR User" -d /tmp perfsonar 2> /dev/null || :

%post common
mkdir -p /var/log/perfsonar
chown perfsonar:perfsonar /var/log/perfsonar
mkdir -p /var/lib/perfsonar/bundles

%post testpoint
echo "perfsonar-testpoint" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}-%{release}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version
#create symlink so we don't litter /etc/security/limits.d with .rpmsave files and similar
ln -sf /etc/perfsonar/toolkit/perfsonar_ulimit.conf /etc/security/limits.d/perfsonar.conf 2> /dev/null
mkdir -p /etc/systemd/system/httpd.service.d
ln -sf /etc/perfsonar/toolkit/perfsonar_ulimit_apache.conf /etc/systemd/system/httpd.service.d/

#copy over default limits if file does not already exist
cp -n %{toolkit_config_base}/pscheduler_limits.conf /etc/pscheduler/limits.conf


#Restart pscheduler daemons to make sure they got all tests, tools, and archivers
%if 0%{?el7}
systemctl daemon-reload &>/dev/null || :
systemctl restart httpd &>/dev/null || :
systemctl restart pscheduler-archiver &>/dev/null || :
systemctl restart pscheduler-runner &>/dev/null || :
systemctl restart pscheduler-scheduler &>/dev/null || :
systemctl restart pscheduler-ticker &>/dev/null || :
%else
/sbin/service httpd restart &>/dev/null || :
/sbin/service pscheduler-archiver restart &>/dev/null || :
/sbin/service pscheduler-runner restart &>/dev/null || :
/sbin/service pscheduler-scheduler restart &>/dev/null || :
/sbin/service pscheduler-ticker restart &>/dev/null || :
%endif

%post core
echo "perfsonar-core" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}-%{release}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version
#configure database
if [ $1 -eq 1 ] ; then
    /usr/lib/perfsonar/scripts/system_environment/configure_esmond new
    /sbin/service httpd restart &>/dev/null || :
fi

%post centralmanagement
echo "perfsonar-centralmanagement" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}-%{release}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version
if [ $1 -eq 1 ] ; then
    /usr/lib/perfsonar/scripts/system_environment/configure_esmond new
fi

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

%files bwctl-compat
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

%define relnum 1
%define toolkit_config_base /etc/perfsonar/toolkit/default_service_configs

Version:        4.0.2.1
Name:           perfsonar
Summary:        Bundles of the perfSONAR Software
Release:        %{relnum}%{?dist}
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
Requires:       pscheduler-core
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
Requires:       libperfsonar-pscheduler-perl
Requires:       libperfsonar-toolkit-perl 
Requires:       libperfsonar-perl 
Requires:       httpd-wsgi-socket
Requires:       perfsonar-tools
Requires:       perfsonar-oppd-bwctl
Requires:       perfsonar-oppd-owamp
Requires:       perfsonar-lsregistrationdaemon
Requires:       perfsonar-toolkit-install
Requires:       perfsonar-meshconfig-agent
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
Requires:               perfsonar-toolkit-compat-database
Requires:               esmond >= 2.1
Requires:               esmond-database-postgresql95
Requires:               perfsonar-toolkit-install
Requires(post):         perfsonar-toolkit-compat-database
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
Requires:       perfsonar-lsregistrationdaemon
Requires:       perfsonar-meshconfig-jsonbuilder
Requires:       perfsonar-meshconfig-guiagent
Requires:       perfsonar-toolkit-compat-database
Requires:       maddash
Requires:       esmond >= 2.1
Requires:       esmond-database-postgresql95
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
echo "perfsonar-testpoint" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}-%{release}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version
#create symlink so we don't litter /etc/security/limits.d with .rpmsave files and similar
ln -sf /etc/perfsonar/toolkit/perfsonar_ulimit.conf /etc/security/limits.d/perfsonar.conf 2> /dev/null

#copy over default limits if file does not already exist
cp -n %{toolkit_config_base}/pscheduler_limits.conf /etc/pscheduler/limits.conf


#Restart pscheduler daemons to make sure they got all tests, tools, and archivers
%if 0%{?el7}
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

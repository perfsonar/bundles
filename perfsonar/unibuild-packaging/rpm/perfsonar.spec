%define perfsonar_auto_version 5.1.2
%define perfsonar_auto_relnum 1
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
%if 0%{?el7}
Requires:       ntp
%else
Requires:       chrony
%endif

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
Requires:       perfsonar-toolkit-web-services
Requires:       perfsonar-host-metrics
Requires(post): perfsonar-toolkit-install
Obsoletes:      perfSONAR-Bundles-TestPoint
Provides:       perfSONAR-Bundles-TestPoint

%description testpoint
Perform regularly scheduled perfSONAR measurements and store the results remotely.

%package core
Summary:                perfSONAR scheduled testing and storage tools
Group:                  Applications/Communications
Requires:               perfsonar-testpoint
Requires:               perfsonar-archive
Requires:               perfsonar-toolkit-install
Requires:               perfsonar-toolkit-archive-utils
Obsoletes:              perfSONAR-Bundles-Core
Provides:               perfSONAR-Bundles-Core

%description core
Perform regularly scheduled perfSONAR measurements and store the results locally.

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
systemctl daemon-reload &>/dev/null || :
systemctl restart httpd &>/dev/null || :
systemctl restart pscheduler-archiver &>/dev/null || :
systemctl restart pscheduler-runner &>/dev/null || :
systemctl restart pscheduler-scheduler &>/dev/null || :
systemctl restart pscheduler-ticker &>/dev/null || :

%post core
echo "perfsonar-core" > /var/lib/perfsonar/bundles/bundle_type
echo "%{version}-%{release}" > /var/lib/perfsonar/bundles/bundle_version
chmod 644 /var/lib/perfsonar/bundles/bundle_type
chmod 644 /var/lib/perfsonar/bundles/bundle_version
#configure database
if [ $1 -eq 1 ] ; then
    /sbin/service httpd restart &>/dev/null || :
fi

%files tools
%defattr(0644,perfsonar,perfsonar,0755)

%files testpoint
%defattr(0644,perfsonar,perfsonar,0755)

%files core
%defattr(0644,perfsonar,perfsonar,0755)

%changelog
* Fri Oct 15 2021 daniel.neto@rnp.br
- Add logstash configuration
* Mon Jul 14 2015 andy@es.net
- common bundle
* Mon Jul 06 2015 adelvaux@man.poznan.pl
- Tools bundle
* Wed Mar 25 2015 sowmya@es.net
- Core bundle
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle

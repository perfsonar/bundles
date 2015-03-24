%define relnum 1 
%define disttag pSPS

Version:		3.4.0
Name:			perfSONAR_PS-Bundles
Summary:		Bundles of the perfSONAR-PS Software
Release:		%{relnum}.%{disttag}
License:		Distributable, see LICENSE
Group:			Applications/Communications
URL:			http://psps.perfsonar.net/
BuildArch:		noarch

%description
Various bundles of the perfSONAR-PS Software

%package TestPoint
Summary:		pS-Performance Toolkit Bundle - minimal test end point
Group:			Applications/Communications
Requires:               Internet2-repo
Requires:		bwctl-client
Requires:		bwctl-server
Requires:		ndt-client
Requires:		owamp-client
Requires:		owamp-server
Requires:		nuttcp
Requires:		iperf
Requires:               iperf3
Requires:		ntp
Requires:		perl-perfSONAR_PS-LSRegistrationDaemon
Requires:               perl-perfSONAR_PS-RegularTesting
Requires:               perl-perfSONAR_PS-Toolkit-Install-Scripts

%description TestPoint
The perfSONAR Toolkit - minimal test point bundle

%package CentralManagement
Summary:		pS-Performance Toolkit Bundle - Central Management
Group:			Applications/Communications
Requires:               Internet2-repo
Requires:               datastax-repo
Requires:		perl-perfSONAR_PS-MeshConfig-Agent
Requires:               maddash
Requires:               esmond

%description CentralManagement
The perfSONAR Toolkit - Central Management

%post

%files
%defattr(0644,perfsonar,perfsonar,0755)

%files TestPoint
%defattr(0644,perfsonar,perfsonar,0755)

%files CentralManagement
%defattr(0644,perfsonar,perfsonar,0755)

%changelog
* Tue Mar 24 2015 sowmya@es.net
- Testpoint and CentralManagement bundle

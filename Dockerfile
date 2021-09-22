FROM centos/systemd:latest

##add perfSONAR nightly repo for perfsonar dependencies
RUN rpm -hUv http://software.internet2.edu/rpms/el7/x86_64/latest/packages/perfSONAR-repo-nightly-minor-0.10-1.noarch.rpm

#Install build environment dependencies
RUN yum update -y && \
    yum install -y epel-release make rpmbuild rpmdevtools && \
    yum clean all && \
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS} && \
    echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

# Copy code to /app
COPY . /app

#Build RPMs
RUN cd /app && \
    rpmbuild -bs perfsonar.spec && \
    rpmbuild -ba perfsonar.spec

#shared volumes
VOLUME /sys/fs/cgroup

CMD ["/usr/sbin/init"]
# Makefile for perfSONAR bundles
#
PACKAGE=perfsonar-bundles
DC_CMD_BASE=docker-compose
DC_CMD=${DC_CMD_BASE} -p ${PACKAGE}

centos7:
	mkdir -p ./artifacts/centos7
	${DC_CMD} -f docker-compose.yml up --build --no-start centos7
	docker cp ${PACKAGE}_centos7_1:/root/rpmbuild/SRPMS ./artifacts/centos7/SRPMS
	docker cp ${PACKAGE}_centos7_1:/root/rpmbuild/RPMS/noarch ./artifacts/centos7/RPMS
FROM centos:centos7
USER root
ENV PORT 5000
RUN yum -y update; yum clean all
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all
RUN useradd user
ADD tstamp.py requirements.txt entrypoint.sh /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
USER user
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []

FROM centos:centos7.6.1810
USER root
ENV PORT 5000
RUN yum -y install epel-release; yum clean all
RUN yum -y install python3-pip; yum clean all
RUN useradd user
ADD tstamp.py requirements.txt entrypoint.sh /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE $PORT
USER user
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []

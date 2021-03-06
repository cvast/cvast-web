FROM ubuntu:14.04
USER root

# Setting default environment variables
ENV WEB_ROOT=/cvast_web
ENV WEB_APP_NAME=cvast_arches

ENV INSTALL_DIR=/install

ENV DJANGO_MODE=PROD
ENV DJANGO_DEBUG=False

# Install dependencies
RUN apt-get update -y &&\
	apt-get install -y wget &&\
	apt-get install -y build-essential &&\
	apt-get install -y libxml2-dev &&\
	apt-get install -y libjson0-dev &&\
	apt-get install -y libproj-dev &&\
	apt-get install -y xsltproc docbook-xsl &&\
	apt-get install -y docbook-mathml &&\
	apt-get install -y libgdal1-dev &&\
	apt-get install -y python-setuptools &&\
	apt-get install -y python-dev &&\
	apt-get install -y libffi-dev &&\
	apt-get install -y libpq-dev &&\
	apt-get install -y dos2unix &&\
	easy_install pip &&\
	pip install SPARQLWrapper \
		requests \
		'Django==1.6.2' \
		'elasticsearch>=1.0.0,<2.0.0' \
		'xlrd==0.9.0' \
		'Pillow==2.4.0' \
		rdflib \
		unicodecsv \
		pyyaml \
		pyshp

# Install postgres, because Arches installer is expecting it
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update -y &&\
	apt-get install -y postgresql-9.4
	
# Remove package list to free up space
RUN rm -rf /var/lib/apt/lists/*

# For debugging with Visual Studio Code
RUN pip install ptvsd


# Root project folder
RUN mkdir ${WEB_ROOT}

# Install the Arches application	
COPY arches ${WEB_ROOT}/arches
WORKDIR	${WEB_ROOT}/arches
RUN	pip install --no-index -e .
# Seemed necessary, received errors without this
RUN python setup.py build
# Seemed necessary, received errors without this	
RUN python setup.py install							


# Install Arches Hip
COPY arches_hip ${WEB_ROOT}/arches_hip
WORKDIR ${WEB_ROOT}/arches_hip
RUN pip install --no-index -e .
# RUN python setup.py build							# Apparently not necessary
# RUN python setup.py install						# Apparently not necessary


# Setup custom app based on Arches Hip
# WORKDIR /${WEB_ROOT}
# RUN arches-app create ${WEB_APP_NAME} --app arches_hip

# Install Elasticsearch
COPY ${WEB_APP_NAME} ${WEB_ROOT}/${WEB_APP_NAME}
WORKDIR ${WEB_ROOT}/${WEB_APP_NAME}





################################################################



# Entrypoint to setup volume mounts
COPY install/web/web_entrypoint.sh ${INSTALL_DIR}/web_entrypoint.sh
RUN chmod -R 700 ${INSTALL_DIR}
RUN dos2unix ${INSTALL_DIR}/*


VOLUME ["${WEB_ROOT}/${WEB_APP_NAME}/${WEB_APP_NAME}/uploadedfiles/files", "${WEB_ROOT}/${WEB_APP_NAME}/${WEB_APP_NAME}/logs"]
EXPOSE 8000
WORKDIR ${WEB_ROOT}/${WEB_APP_NAME}
CMD ${INSTALL_DIR}/web_entrypoint.sh
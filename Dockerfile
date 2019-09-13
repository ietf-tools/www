FROM opensuse/leap

ENV LANG en_US.UTF-8  

RUN zypper -n update && zypper -n install \
        apache2 \
        apache2-devel \
        bind-utils \
        command-not-found \
        coreutils \
        findutils \
        gcc \
        gcc-c++ \
        iputils \
        less \
        lftp \
        net-tools \
        net-tools-deprecated \
        rsync \
        python3 \
        python3-devel \
        python3-pip \
        sudo \
        vim 
        
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 5

EXPOSE 8001:8001

RUN mkdir /code
WORKDIR /code

# Doing this step before copying the whole codebase improves docker's ability to reuse cached layers at build time
COPY --chown=wwwrun:www ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY --chown=wwwrun:www . /code/

RUN mkdir /code/static
RUN chown wwwrun:www /code/static

RUN mkdir /code/logs
RUN chown wwwrun:www /code/logs

ENV DJANGO_SETTINGS_MODULE ietf.settings.production

ENTRYPOINT ./docker-entry.sh


FROM opensuse/leap

RUN zypper -n update && zypper -n install \
        apache2 \
        apache2-devel \
        command-not-found \
        gcc \
        gcc-c++ \
        less \
        net-tools \
        net-tools-deprecated \
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

ENTRYPOINT ./docker-entry.sh


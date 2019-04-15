FROM opensuse/leap

RUN zypper -n update

RUN zypper -n install \
        apache2 \
        apache2-devel \
        gcc \
        gcc-c++ \
        python3 \
        python3-devel \
        python3-pip \
        sudo

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 5

EXPOSE 8001:8001

RUN mkdir /code
WORKDIR /code
COPY --chown=wwwrun:www . /code/

RUN mkdir /code/static
RUN chown wwwrun:www /code/static

RUN mkdir /code/logs
RUN chown wwwrun:www /code/logs

RUN pip install -r requirements.txt

RUN echo "SECRET_KEY='garbage'" > ietf/settings/local.py
ENV DJANGO_SETTINGS_MODULE=ietf.settings.production
RUN ./manage.py runmodwsgi --setup-only --port 8001 --user wwwrun --group www --access-log --server-root /code/mod_wsgi-express-8001 --log-directory /code/logs
RUN rm ietf/settings/local.py

ENTRYPOINT ./docker-entry.sh


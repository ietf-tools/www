# Frontend assets
FROM node:erbium-alpine as frontend

ENV NODE_PATH=/node_modules
ENV PATH="${PATH}:/node_modules/.bin"
RUN mkdir ${NODE_PATH}

COPY yarn.lock \
  package.json \
  /app/

WORKDIR /app

RUN NODE_ENV=development yarn install --modules-folder $NODE_PATH

COPY . /app/
RUN yarn dist

CMD ["yarn", "start", "--prefix", "/app"]

# Base backend
FROM springload/ssm-parent:1.4.1 as ssm-parent

FROM python:3.6-alpine as base
ENV PYCURL_SSL_LIBRARY openssl

RUN apk update && apk add postgresql-libs libevent libjpeg openjpeg zlib

WORKDIR /app

COPY docker/requirements.txt docker/constraints.txt /app/docker/
COPY requirements.txt /app/requirements/main.txt
COPY constraints.txt /app/requirements/constraints.txt

RUN apk update && apk add --virtual build-deps make gcc g++ musl-dev apache2-dev && \
  apk add --virtual build-headers postgresql-dev \
  jpeg-dev \
  zlib-dev \
  openjpeg-dev \
  libevent-dev && \
  cd /app && \
  pip3 install -r docker/requirements.txt && \
  pip3 install -r requirements/main.txt && \
  apk del build-deps build-headers

COPY --from=frontend /app/ /app/

RUN adduser -S www -u 1000 && chown -R www /app


COPY ./ ./

ARG VERSION=dev
ENV APPLICATION_VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.hosting
ENV VERSION=${VERSION}
ENV ENVIRONMENT unknown
ENV PROJECT wagtail_website

# base app stage
FROM base as base-app

# production stage
FROM base-app as app

COPY --from=ssm-parent /usr/bin/ssm-parent /usr/bin/ssm-parent

USER www
ENTRYPOINT ["/usr/bin/ssm-parent", "run", "-e", "-p", "/$PROJECT/common/", "-p", "/$PROJECT/$ENVIRONMENT/", "-n", "/$PROJECT/$ENVIRONMENT/ssm", "-r",  "--"]
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "ietf.wsgi" ]

# Huey stage
FROM app as tasks
CMD ["python", "/app/manage.py",  "run_huey"]

# development stage
FROM base-app as app-dev
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.dev

ADD https://raw.githubusercontent.com/mrako/wait-for/d9699cb9fe8a4622f05c4ee32adf2fd93239d005/wait-for /usr/local/bin/
RUN chmod +rx /usr/local/bin/wait-for

ENTRYPOINT ["wait-for", "database:5432", "--"]
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "--reload", "ietf.wsgi" ]

# ---------------------------------------------------------------------
# FRONTEND
# ---------------------------------------------------------------------
# Frontend assets get compiled first
FROM node:20-alpine as frontend

ENV NODE_PATH=/node_modules
ENV PATH="${PATH}:/node_modules/.bin"
RUN mkdir ${NODE_PATH}
# for accessibility tests
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser
RUN apk add --no-cache chromium ca-certificates

# Copy node reqs first to benefit from Docker caching
COPY yarn.lock \
  package.json \
  /app/

WORKDIR /app

RUN NODE_ENV=development yarn install --modules-folder $NODE_PATH

COPY . /app/
RUN yarn dist

CMD ["yarn", "start"]

# ---------------------------------------------------------------------
# BASE
# ---------------------------------------------------------------------
# Base backend
FROM python:3.12-alpine as base
ENV PYCURL_SSL_LIBRARY openssl

RUN apk update && apk add postgresql-libs postgresql-client libevent libjpeg openjpeg zlib

WORKDIR /app

# Copy Python reqs to benefit from Docker caching
COPY requirements ./requirements

# Install build dependencies, then Python requirements, then remove build dependencies
# to reduce the resulting image size
RUN apk update && apk add --virtual build-deps make gcc g++ musl-dev apache2-dev && \
  apk add --virtual build-headers postgresql-dev \
  jpeg-dev \
  zlib-dev \
  openjpeg-dev \
  libevent-dev && \
  cd /app && \
  pip3 install -r requirements/base.txt -r requirements/docker.txt && \
  apk del build-deps build-headers

RUN adduser -S www -u 1000 && chown -R www /app

# here we copy the project code along with compiled static assets
COPY --from=frontend /app/ /app/


ARG VERSION=dev
ENV APPLICATION_VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.base
ENV VERSION=${VERSION}
ENV ENVIRONMENT unknown
ENV PROJECT wagtail_website

USER www

# ---------------------------------------------------------------------
# APP
# ---------------------------------------------------------------------
# base app (hosted elsewhere, not on AWS)
FROM base as app
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "ietf.wsgi" ]

# ---------------------------------------------------------------------
# APP - DEV
# ---------------------------------------------------------------------
# development stage
FROM base as app-dev
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.dev
COPY docker/init-dev.sh /app/docker/

ADD https://raw.githubusercontent.com/mrako/wait-for/d9699cb9fe8a4622f05c4ee32adf2fd93239d005/wait-for /usr/local/bin/
USER root
RUN apk add --no-cache bash postgresql-dev
RUN pip3 install -r requirements/dev.txt
RUN chmod +rx /usr/local/bin/wait-for
USER www

# wait-for script waits until the database is ready and reachable
# and then it runs the migrations and actual process
ENTRYPOINT ["wait-for", "database:5432", "--"]
CMD ["/app/docker/init-dev.sh"]

# ---------------------------------------------------------------------
# APP - TEST
# ---------------------------------------------------------------------
# test stage
FROM base as app-test
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.dev
COPY docker/init-test.sh /app/docker/

ADD https://raw.githubusercontent.com/mrako/wait-for/d9699cb9fe8a4622f05c4ee32adf2fd93239d005/wait-for /usr/local/bin/
USER root
RUN pip3 install -r requirements/dev.txt
RUN chmod +rx /usr/local/bin/wait-for
USER www

# wait-for script waits until the database is ready and reachable
# and then it runs the migrations and tests
ENTRYPOINT ["wait-for", "database:5432", "--"]
CMD ["/app/docker/init-test.sh"]

# ---------------------------------------------------------------------
# APP - SANDBOX
# ---------------------------------------------------------------------
# sandbox stage
FROM base as app-sandbox

USER root

RUN apk update && apk add --no-cache nginx supervisor

COPY docker/nginx-sandbox.conf /etc/nginx/http.d/default.conf
COPY docker/supervisord-sandbox.conf /app/supervisord.conf

RUN mkdir -p /app/media

CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]

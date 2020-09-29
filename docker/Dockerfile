# Frontend assets get compiled first
FROM node:erbium-alpine as frontend

ENV NODE_PATH=/node_modules
ENV PATH="${PATH}:/node_modules/.bin"
RUN mkdir ${NODE_PATH}

# Copy node reqs first to benefit from Docker caching
COPY yarn.lock \
  package.json \
  /app/

WORKDIR /app

RUN NODE_ENV=development yarn install --modules-folder $NODE_PATH

COPY . /app/
RUN yarn dist

CMD ["yarn", "start", "--prefix", "/app"]

# Needed for hosting on AWS
FROM springload/ssm-parent:1.4.1 as ssm-parent

# Base backend
FROM python:3.6-alpine as base
ENV PYCURL_SSL_LIBRARY openssl

RUN apk update && apk add postgresql-libs libevent libjpeg openjpeg zlib

WORKDIR /app

# Copy Python reqs to benefit from Docker caching
COPY docker/requirements.txt docker/constraints.txt /app/docker/
COPY requirements.txt /app/requirements/main.txt
COPY constraints.txt /app/requirements/constraints.txt

# Install build dependencies, then Python requirements, then remove build dependencies
# to reduce the resulting image size
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

RUN adduser -S www -u 1000 && chown -R www /app

# here we copy the project code along with compiled static assets
COPY --from=frontend /app/ /app/


ARG VERSION=dev
ENV APPLICATION_VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.hosting
ENV VERSION=${VERSION}
ENV ENVIRONMENT unknown
ENV PROJECT wagtail_website

USER www

# AWS hosting stages
FROM base as aws-app

# ssm-parent is needed for dynamic env-variable configuration on AWS.
# It just reads encrypted secrets from AWS SSM Parameter Store and exposes them
# as the environment variables to the process inside of the container
COPY --from=ssm-parent /usr/bin/ssm-parent /usr/bin/ssm-parent

ENTRYPOINT ["/usr/bin/ssm-parent", "run", "-e", "-p", "/$PROJECT/common/", "-p", "/$PROJECT/$ENVIRONMENT/", "-n", "/$PROJECT/$ENVIRONMENT/ssm", "-r",  "--"]
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "ietf.wsgi" ]

# base app (hosted elsewhere, not on AWS)
FROM base as app
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "ietf.wsgi" ]

# development stage
FROM base as app-dev
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.dev

ADD https://raw.githubusercontent.com/mrako/wait-for/d9699cb9fe8a4622f05c4ee32adf2fd93239d005/wait-for /usr/local/bin/
USER root
RUN chmod +rx /usr/local/bin/wait-for
USER www

# wait-for script waits until the database is ready and reachable
# and then it runs the actual process
ENTRYPOINT ["wait-for", "database:5432", "--"]
CMD ["/usr/local/bin/gunicorn", "--config", "/app/docker/gunicorn.py", "--reload", "ietf.wsgi" ]

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
FROM python:3.12-bookworm as base
ENV PYCURL_SSL_LIBRARY openssl
ENV APT_BUILD_DEPS "build-essential libpq-dev"

WORKDIR /app

# Copy Python reqs to benefit from Docker caching
COPY requirements ./requirements

# Install build dependencies, then Python requirements, then remove build dependencies
# to reduce the resulting image size
RUN <<EOF
    set -ex
    apt-get update -qq
    apt-get install -qq postgresql-client netcat-openbsd $APT_BUILD_DEPS
    cd /app
    pip3 install -r requirements/base.txt -r requirements/docker.txt
    apt-get purge -qq $APT_BUILD_DEPS
    apt-get autoremove --purge -qq
    rm -rf /var/lib/apt/lists/*
EOF

RUN <<EOF
    set -ex
    useradd www --create-home
    chown -R www /app
EOF

# here we copy the project code along with compiled static assets
COPY --from=frontend /app/ /app/


ARG VERSION=dev
ENV APPLICATION_VERSION=${VERSION}
ENV DJANGO_SETTINGS_MODULE ietf.settings.docker.base
ENV VERSION=${VERSION}
ENV ENVIRONMENT unknown
ENV PROJECT www

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
RUN <<EOF
    set -ex
    apt-get update -qq
    apt-get install -qq $APT_BUILD_DEPS
EOF
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

RUN <<EOF
    set -ex
    apt-get update -qq
    apt-get install -qq nginx supervisor
    rm -rf /var/lib/apt/lists/*
EOF

COPY docker/nginx-sandbox.conf /etc/nginx/sites-enabled/default
COPY docker/supervisord-sandbox.conf /app/supervisord.conf

COPY docker/init.sh /app/init.sh
RUN chmod +x /app/init.sh

RUN mkdir -p /app/media

# Configure environment variables (each with a placeholder) required
# to bootstrap Django, so that collectstatic can run successfully
RUN APP_SECRET_KEY="abcdef" \
    DATABASE_URL="postgresql://userspec@hostspec/dbname?paramspec" \
    python /app/manage.py collectstatic --no-input

CMD ["./init.sh"]

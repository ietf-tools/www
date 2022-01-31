<div align="center">
    
<img src="https://raw.githubusercontent.com/ietf-tools/common/main/assets/logos/ietf-wagtail-site-logo.svg" alt="IETF Wagtail Website" width="600" />
    
[![Release](https://img.shields.io/github/release/ietf-tools/wagtail_website.svg?style=flat&maxAge=360)](https://github.com/ietf-tools/wagtail_website/releases)
[![License](https://img.shields.io/github/license/ietf-tools/wagtail_website)](https://github.com/ietf-tools/wagtail_website/blob/main/LICENSE)
[![CircleCI](https://img.shields.io/circleci/build/github/ietf-tools/wagtail_website?label=Circle%20CI%20Build)]()
[![Docker Images](https://img.shields.io/badge/docker%20images-github-blue?logo=docker&logoColor=white)](https://github.com/ietf-tools/wagtail_website/pkgs/container/wagtail_website)
    
##### A customized CMS for the IETF website
    
</div>

- [Changelog](https://github.com/ietf-tools/wagtail_website/releases)
- [Contributing](https://github.com/ietf-tools/wagtail_website/blob/main/CONTRIBUTING.md)
- [Install](#install)
- [Requirements](#requirements)
- [Website *(Production)*](https://www.ietf.org)
- [Website *(Dev)*](https://wwwdev.ietf.org)

---

## Requirements

- **macOS / Windows**: Docker for Desktop
- **Linux**: Docker + Docker-Compose

## Install

### Quick start

First, clone this repository.

#### Run in Docker locally

This project uses Docker to build and run the code, both frontend and backend.
So the only requirement to run it locally is a recent version of Docker with docker-compose.

##### How to run (with a database dump)

1. Obtain a recent database dump with name like `ietfa.torchbox.*.gz` and place in `docker/database/` directory. Otherwise, it will start with a fresh database.
2. Obtain and unarchive media files into `media/` folder.
3. Run `docker-compose up`. It will build and start the frontend builder (`yarn run start`) and the backend (`python manage.py runserver` analog), along with a Postgresql database. The first run will take a while because the database dump needs to be restored.
4. After the frontend compilation finishes, the website should become available at http://localhost:8001
5. Create a super user on **Python application** docker instance to access http://localhost:8001/admin
```sh
docker exec -ti wagtail_website_application_1 python manage.py createsuperuser
```
6. To destroy everything (i.e. start the database from scratch) run `docker-compose down`.

##### How to run (without a database dump)

1. Run `docker-compose up`. It will build and start the frontend builder (`yarn run start`) and the backend (`python manage.py runserver` analog), along with a Postgresql database. The first run will take a while because the database dump needs to be restored.
2. Create an admin user
```sh
docker exec -ti wagtail_website_application_1 python manage.py createsuperuser
```
3. Log into http://localhost:8001/admin
4. Create a new "Home Page" (page type must be `Home Page`) and **publish**.
5. Go to http://localhost:8001/admin/sites/ and select **localhost**.
6. Select the new "Home Page" as the **root page** and **save**.
7. The website should become available at http://localhost:8001
8. To destroy everything (i.e. start the database from scratch) run `docker-compose down`.

##### Backend details

The backend configuration resides in `ietf/settings/docker`, inheriting some settings from `base.py`. Configuration is done with environment variables with sane checks, i.e. if a variable is required but not set, the application won't start.

#### On the frontend (separate from Docker if needed)

Note: Running these steps before the Docker instructions above may prevent the frontend docker instance to run properly.

Install [NVM](https://github.com/nvm-sh/nvm) and [Yarn](https://yarnpkg.com/) and then run these commands from the repo directory,

First, install dependencies:

```sh
# Make sure you use the right node version.
nvm install
nvm use
# Install project dependencies
yarn install
```

Then, build the frontend static files using one of these commands

```sh
# Builds and watches the frontend assets (use this when developing).
yarn run start

# Builds frontend development (non-optimized) assets, without watching
yarn run build

# Builds frontend production assets.
yarn run dist
```

Other available commands can be viewed with

```sh
yarn run
```

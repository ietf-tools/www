<div align="center">
    
<img src="https://raw.githubusercontent.com/ietf-tools/common/main/assets/logos/wagtail-site.svg" alt="IETF Wagtail Website" height="125" />
    
[![Release](https://img.shields.io/github/release/ietf-tools/www.svg?style=flat&maxAge=360)](https://github.com/ietf-tools/www/releases)
[![License](https://img.shields.io/github/license/ietf-tools/www)](https://github.com/ietf-tools/www/blob/main/LICENSE)
[![Docker Images](https://img.shields.io/badge/docker%20images-github-blue?logo=docker&logoColor=white)](https://github.com/ietf-tools/www/pkgs/container/www)
    
##### A customized CMS for the IETF website
    
</div>

-   [Changelog](https://github.com/ietf-tools/www/releases)
-   [Contributing](https://github.com/ietf-tools/www/blob/main/CONTRIBUTING.md)
-   [Install](#install)
-   [Requirements](#requirements)
-   [Deployment](#deployment)

---

## Requirements

-   **macOS / Windows**: Docker for Desktop
-   **Linux**: Docker + Docker-Compose

## Install

### Quick start

First, clone this repository.

#### Run in Docker locally

This project uses Docker to build and run the code, both frontend and backend.
So the only requirement to run it locally is a recent version of Docker with docker-compose.

##### How to run (with a database dump)

1. Obtain a recent database dump with name like `ietfa.*.gz` and place in `docker/database/` directory. Otherwise, it will start with a fresh database.
2. Obtain and unarchive media files into `media/` folder.
3. Run `docker compose up`. It will build and start the frontend builder (`yarn run start`) and the backend (`python manage.py runserver` analog), along with a Postgresql database. The first run will take a while because the database dump needs to be restored.
4. After the frontend compilation finishes, the website should become available at http://localhost:8001
5. Create a super user on **Python application** docker instance to access http://localhost:8001/admin

    ```sh
    docker exec -ti www-application-1 python manage.py createsuperuser
    ```

6. To destroy everything (i.e. start the database from scratch) run `docker compose down`.

##### How to run (without a database dump)

1. Run `docker compose up`. It will build and start the frontend builder (`yarn run start`) and the backend (`python manage.py runserver` analog), along with a Postgresql database. The first run will take a while because the database dump needs to be restored.
2. Create an admin user

    ```sh
    docker exec -ti www-application-1 python manage.py createsuperuser
    ```

3. Log into http://localhost:8001/admin
4. Create a new "Home Page" (page type must be `Home Page`) and **publish**.
5. Go to http://localhost:8001/admin/sites/ and select **localhost**.
6. Select the new "Home Page" as the **root page** and **save**.
7. The website should become available at http://localhost:8001
8. To destroy everything (i.e. start the database from scratch) run `docker compose down`.

##### Backend details

The backend configuration resides in `ietf/settings/docker`, inheriting some settings from `base.py`. Configuration is done with environment variables with sane checks, i.e. if a variable is required but not set, the application won't start.

#### Analytics settings

To send analytics data to Matomo set the following configuration options in the local settings file.
```
MATOMO_DOMAIN_PATH = "analytics.ietf.org"
MATOMO_SITE_ID = "<site id>"
```

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

#### Multi site setup

This repo contains code for both the IETF and IAB websites, which are intended to run as separate sites. If you don't have a DB dump, or your dump does not have the IAB site set up, these are the steps you need to have a paralell site running:

-   Set up a page using the IAB homepage template at the root level (`/admin/pages`)
-   Configure a site with that page as its root (`http://localhost:8001/admin/sites/`)
-   In settings -> layout settings (http://localhost:8001/admin/settings/utils/layoutsettings/2/), select your new site and make sure that the base template is set to IAB
-   Header and footer links are populated in the same way as the IETF website. The header contains pages that have the 'show in menu' checkbox ticked in the 'promote' tab. Footer links are set in settings -> footer links.

## Upgrading dependencies

Dependencies are managed using [pip-tools](https://pip-tools.readthedocs.io/en/stable/). They are specified in `requirements/*.in` and version-pinned in `requirements/*.txt`. To update the pins, run:

```sh
docker compose run --rm application requirements/compile -U
```

## Deployment

Production: [IETF](https://www.ietf.org/), [IAB](https://temporary.iab.org/)

Staging: [IETF](https://wwwstaging.ietf.org/), [IAB](https://wwwstaging.iab.org/)

Dev _(automatically build from **main** branch)_: https://ws-main.dev.ietf.org/

### Testing changes on sandbox

* Use [Build and release](https://github.com/ietf-tools/www/actions/workflows/build.yml) GHA.
* Select the branch that you want to deploy.
* Make sure **Create Production Release** is **not** ticked.
* Tick **Deploy to Sandbox**.
* Click **Run Workflow** button.

If the `main` branch is selected, changes will be deployed to https://ws-main.dev.ietf.org/

Changes will be available on a subdomain compiled from the branch name if any other branch is selected. If a `/` is present in the branch name, the first part will be stripped off and any other `/` are replaced with `-`. For example, deployment from the `feat/foobar` branch will be available on `https://ws-foobar.dev.ietf.org`, branch `fix/foo-bar` will be available on `https://ws-foo-bar.dev.ietf.org` and branch `fix/foo/bar` will be available on  `https://ws-foo-bar.dev.ietf.org`.

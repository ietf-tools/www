# INSTALL

## Quick start

### Run in Docker locally

This project uses Docker to build and run the code, both frontend and backend.
So the only requirement to run it locally is a recent version of Docker with docker-compose.

#### How to run

1. (Optional) Obtain a recent database dump with name like `ietfa.torchbox.*.gz` and place in `docker/database/` directory. Otherwise, it will start with a fresh database.
2. Obtain and unarchive media files into `media/` folder.
3. Run `docker-compose up`. It will build and start the frontend builder (`yarn run start`) and the backend (`python manage.py runserver` analog), along with a Postgresql database. The first run will take a while because the database dump needs to be restored.
4. After the frontend compilation finishes, the website should become available at http://localhost:8081
5. To destroy everything (i.e. start the database from scratch) run `docker-compose down`.

#### Backend details

The backend configuration resides in `ietf/settings/docker`, inheriting some settings from `base.py`. Configuration is done with environment variables with sane checks, i.e. if a variable is required but not set, the application won't start.

### On the frontend (separate from Docker if needed)

This project uses [nvm](https://github.com/creationix/nvm) and [Yarn](https://yarnpkg.com/lang/en/)

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

Other available commands cand be viewed with

```sh
yarn run
```

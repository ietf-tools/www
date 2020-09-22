# INSTALL

## Quick start

### On the frontend

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

# Developing on the Internet Engineering Task Force (IETF) Website

## Backend Development

This website uses the Wagtail CMS.

### Installing

Documentation for running the backend environment is being written.

You may wish to ask for a database dump before testing.

### Testing

Wagtail is based on Django, and there are many Django-style tests typically named `tests.py` to test templates. These verify that the templates can be compiled (that they don't have syntax errors) and that they are inserting variables.

## Frontend Development

This project uses Bootstrap. The exact version is specified in the `package.json` file.

Please adhere to standard Bootstrap practices where possible rather than adding bespoke code, so that future developers can benefit from Boostrap docs and the broader ecosystem.

### Installing

First, clone this repo.

Install [NVM](https://github.com/nvm-sh/nvm) and [Yarn](https://yarnpkg.com/) and then run these commands from the repo directory,

```bash
nvm install
nvm use
```

This will use NVM to install the correct version of Node for this project, and switch to using that version of Node.

```bash
yarn
```

Running `yarn` without any arguments is an alias for `yarn install`. This will install the packages from `package.json`.

```bash
yarn build
```

This will run Webpack and compile the source files at `ietf/static_src`. The `yarn build` command runs a development build without minification and optimisation (useful for debugging), whereas `yarn dist` will run a production build (with minification).

### Testing

#### Accessibility tests

This command requires a running website which may be your local development site.

```bash
yarn test:accessibility http://localhost:9000
```

Replace "http://localhost:9000" with the URL of your running website.

## Deploying

Deploys to production are intentionally not available as deploy branches.

Deploys to staging may be done by merging to `deploy/staging`.

This environment's domain is private, and is password protected. Ask around for the details.

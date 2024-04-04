# Developing on the Internet Engineering Task Force (IETF) Website

## Contributing

Read [Contributing to IETF Tools projects](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md).

## Backend Development

This website uses the Wagtail CMS.

### Installing

See the [installation instructions](README.md#install)

### Testing

Wagtail is based on Django, and there are many tests, in each app, typically named `tests.py` or `tests/test_*.py`, to test templates and business logic. These verify that the pages render without error and that they contain the expected values.

The testsuite uses [pytest](https://docs.pytest.org/) and [pytest-django](https://pytest-django.readthedocs.io/). You can run the testsuite locally:

```bash
pytest
```

### Linting

To ensure a uniform code style, this project uses [black](https://black.readthedocs.io/en/stable/) and [ruff](https://docs.astral.sh/ruff/). You can install the [pre-commit](https://pre-commit.com) hook to run them automatically when making a git commit:

```bash
pre-commit install
```

## Frontend Development

This project uses Bootstrap. The exact version is specified in the `package.json` file.

Please adhere to standard Bootstrap practices where possible rather than adding bespoke code, so that future developers can benefit from Boostrap docs and the broader ecosystem.

### Installing

See the [installation instructions](README.md#install) to get the website running on your local machine.

If you need to inspect the generated files outside of Docker, you can run these commands:

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

Note that `ietf/static_src` will compile HTML templates into `ietf/static`, and this includes Wagtail templates such as `base.html`. Webpack will add CSS and JS tags.

### Testing

#### Accessibility tests

This command requires a running website which may be your local development site.

```bash
yarn test:accessibility http://localhost:8001
```

Replace "`http://localhost:8001`" with the URL of your running website.

## Deploying

See the [deployment section](README.md#deployment)

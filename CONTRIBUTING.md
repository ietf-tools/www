# Developing on the Internet Engineering Task Force (IETF) Website

## Backend Development

This website uses the Wagtail CMS.

### Installing

See the [installation instructions](install.md#install)

### Testing

Wagtail is based on Django, and there are many Django-style tests typically named `tests.py` to test templates. These verify that the templates can be compiled (that they don't have syntax errors) and that they are inserting variables.

## Frontend Development

This project uses Bootstrap. The exact version is specified in the `package.json` file.

Please adhere to standard Bootstrap practices where possible rather than adding bespoke code, so that future developers can benefit from Boostrap docs and the broader ecosystem.

### Installing

See the [installation instructions](install.md#install) to get the website running on your local machine.

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

This project uses deploy branches.

Deploys to production are intentionally unavailable via deploy branches.

Deploys to preview environments are automated via CircleCI. Use your GitHub credentials to sign in to watch deploys and look for failing tests.

CircleCI is configured to run new site builds, to run tests, and (if the tests pass) to deploy.

Deploys to preview may be done by merging to `deploy/preview`.

Eg,

```bash
git push origin main:deploy/preview
```

This would push `main` to `deploy/preview` and trigger a build on CircleCI.

```bash
git push origin feature/my-feature:deploy/preview
```

This would deploy your feature branch `feature/my-feature` to `deploy/preview`.

The preview environment's domain is private, and is password protected. Ask around for the details.

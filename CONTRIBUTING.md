# Developing on the Internet Engineering Task Force (IETF) Website

## Backend Development

This website uses the Wagtail CMS.

### Installing

See the [installation instructions](README.md#install)

### Testing

Wagtail is based on Django, and there are many Django-style tests typically named `tests.py` to test templates. These verify that the templates can be compiled (that they don't have syntax errors) and that they are inserting variables.

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

## Contribututing

Read [Contributing to IETF Tools projects](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md).
For this project treat `deploy/preview` brach as `main`.

## Running Kubernetes Locally

### Prerequisites

-   `kubectl`

    See [Install Tools](https://kubernetes.io/docs/tasks/tools/) (kubernetes.io) for more info.

-   `minikube`

    See [Install Tools](https://kubernetes.io/docs/tasks/tools/) (kubernetes.io) for more info.

-   `helm`

    See [Installing Helm](https://helm.sh/docs/intro/install/) (helm.sh) for more info.

-   Docker image: `postgres`

    ``` bash
    docker pull postgres:14.6-alpine
    ```

-   Database backup: `wagtail_backup_latest.gz`

    ``` bash
    gunzip wagtail_backup_latest.gz
    ```

    Note: The name of your backup file will be different.

### Quick Start

1.  Start a `minikube` cluster unless running already.

    ``` bash
    minikube status
    ```

    ``` bash
    minikube start
    ```

2.  Run a PostgreSQL instance in a new container.

    ``` bash
    docker run --name my-postgres \
           -v $(pwd)/wagtail_backup_latest:/wagtail_backup_latest \
           -v pgdata:/var/lib/postgresql/data \
           -e POSTGRES_PASSWORD=postgres \
           -p 5432:5432 \
           postgres:14.6-alpine
    ```

3.  Start a new `bash` session in the container.

    ``` bash
    docker exec -it 188fcfec0bf9 bash
    ```

    where `188fcfec0bf9` is the ID of the container.

    1.  (Required only once) Using `psql`, create a new database called `wagtail`, and a new role called `www_iab`.

        ``` bash
        psql -U postgres
        ```

        ``` sql
        CREATE DATABASE wagtail;
        CREATE ROLE www_iab WITH LOGIN PASSWORD 'www_iab';
        ```

        ``` text
        \q
        ```

    2.  (Required only once) Restore `wagtail_backup_latest` to the `wagtail` database using `pg_restore`.

        ``` bash
        pg_restore -U postgres -d wagtail wagtail_backup_latest
        ```

4.  Run

    ``` bash
    helm install wagtail helm
    ```

    to install the Helm chart.

5.  Initiate a port-forwarding session for the pod that is running the `wagtail` service.

    ``` bash
    kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
    ```

    e.g.

    ``` bash
    kubectl --namespace default port-forward wagtail-wagtail-5bf8f48bf5-28dvr 8080:8000
    ```

6.  Go to localhost:8080 on your web browser, and perform basic testing.

7.  Create an admin user.

    ``` bash
    kubectl exec -it $POD_NAME --container wagtail -- python manage.py createsuperuser
    ```

    e.g.

    ``` bash
    kubectl exec -it wagtail-wagtail-845c6b54b5-dkfqw --container wagtail -- python manage.py createsuperuser
    ```

8.  Using the admin username and password, log in to localhost:8080/admin.

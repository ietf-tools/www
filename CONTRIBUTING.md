# Developing on the Internet Engineering Task Force (IETF) Website

## Contributing

Read [Contributing to IETF Tools projects](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md).

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

-   Database backup: `www_backup_latest.gz`

    ``` bash
    gunzip www_backup_latest.gz
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
           --rm \
           -v $(pwd)/www_backup_latest:/www_backup_latest \
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

    1.  (Required only once) Using `psql`, create a new database called `www`, and a new role called `www_iab`.

        ``` bash
        psql -U postgres
        ```

        ``` sql
        CREATE DATABASE www;
        CREATE ROLE www_iab WITH LOGIN PASSWORD 'www_iab';
        ```

        ``` text
        \q
        ```

    2.  (Required only once) Restore `www_backup_latest` to the `www` database using `pg_restore`.

        ``` bash
        pg_restore -U postgres -d www www_backup_latest
        ```

    3.  Check extensions installed in the `www` database.

        ``` bash
        psql -U postgres
        ```

        ``` text
        \c www
        ```

        ``` text
        \dx
        ```

        ``` text
                                                    List of installed extensions
                Name        | Version |   Schema   |                              Description
        --------------------+---------+------------+------------------------------------------------------------------------
         adminpack          | 2.1     | pg_catalog | administrative functions for PostgreSQL
         amcheck            | 1.3     | public     | functions for verifying relation integrity
         bloom              | 1.0     | public     | bloom access method - signature file based index
         btree_gin          | 1.3     | public     | support for indexing common datatypes in GIN
         btree_gist         | 1.6     | public     | support for indexing common datatypes in GiST
         citext             | 1.6     | public     | data type for case-insensitive character strings
         fuzzystrmatch      | 1.1     | public     | determine similarities and distance between strings
         pageinspect        | 1.9     | public     | inspect the contents of database pages at a low level
         pg_buffercache     | 1.3     | public     | examine the shared buffer cache
         pg_freespacemap    | 1.2     | public     | examine the free space map (FSM)
         pg_stat_statements | 1.9     | public     | track planning and execution statistics of all SQL statements executed
         pg_trgm            | 1.6     | public     | text similarity measurement and index searching based on trigrams
         pg_visibility      | 1.2     | public     | examine the visibility map (VM) and page-level visibility info
         pgrowlocks         | 1.2     | public     | show row-level locking information
         pgstattuple        | 1.5     | public     | show tuple-level statistics
         plpgsql            | 1.0     | pg_catalog | PL/pgSQL procedural language
        (16 rows)
        ```

        Note: The `adminpack` extension is not available in RDS, therefore it will not be included in future database snapshots. See [Extensions supported for RDS for PostgreSQL 14](https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html#postgresql-extensions-14x) for more information.

4.  Run

    ``` bash
    helm install www helm
    ```

    to install the Helm chart.

5.  Initiate a port-forwarding session for the pod that is running the `wagtail` service.

    ``` bash
    kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
    ```

    e.g.

    ``` bash
    kubectl --namespace default port-forward www-wagtail-69f957f5d6-ppfsd 8080:8000
    ```

6.  Go to localhost:8080 on your web browser, and perform basic testing.

7.  Create an admin user.

    ``` bash
    kubectl exec -it $POD_NAME --container www -- python manage.py createsuperuser
    ```

    e.g.

    ``` bash
    kubectl exec -it www-wagtail-69f957f5d6-ppfsd --container www -- python manage.py createsuperuser
    ```

8.  Using the admin username and password, log in to localhost:8080/admin.

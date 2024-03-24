# WWW Deploy to Container Tool

This tool takes a docker image and deploys it to a container, along with its own database container.

## Requirements

- Node `16.x` or later
- Docker

## Usage

1. From the `dev/deploy-to-container` directory, run the command:
```sh
npm install
```
3. From the project root directory (back up 2 levels), run the command: (replacing the `branch` and `domain` arguments)
```sh
node ./dev/deploy-to-container/cli.js --branch main --domain something.com
```

A container named `ws-app-BRANCH` and `ws-db-BRANCH` (where BRANCH is the argument provided above) will be created.

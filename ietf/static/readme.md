# Static files readme

Needed to implement a fix for tickets 182 and 183 that require transpiled JS to work in IE11. Here's the stripped down tooling from DIBB looking to process just the `main.js` file.

## Usage

run `yarn install` from this folder `ietf/static/`.

Compile JS with `yarn compile:js:dev` or `yarn compile:js:prod`

Watch JS with `yarn compile:js:watch`

## Notes

Be aware this will only transpile `js-src/main.js` and replace `js/main.js` not any other js files in the repo.
const { AxePuppeteer } = require('@axe-core/puppeteer');
const puppeteer = require('puppeteer');
const colorJson = require('color-json');

const baseUrl = 'https://www.ietf.org/'; // @TODO get this from environment variables

const testPaths = ['/'];

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setBypassCSP(true);
    let hasSeriousViolations = false;

    for (let i = 0; i < testPaths.length; i++) {
        const testPath = testPaths[i];
        const url = new URL(testPath, baseUrl).toString();

        console.log(url);
        await page.goto(url);
        const allResults = await new AxePuppeteer(page).analyze();
        const seriousViolations = allResults.violations.filter(
            (violation: any) => violation.impact === 'serious',
        );
        const otherViolations = allResults.violations.filter(
            (violation: any) => violation.impact !== 'serious',
        );

        if (seriousViolations.length > 0 || otherViolations.length > 0) {
            console.log(`Testing ${url} found violations`);
        } else {
            console.log(`No violations at ${url}`);
        }

        if (seriousViolations.length > 0) {
            console.error(colorJson(seriousViolations));
        }

        if (otherViolations.length > 0) {
            console.info('Other violations: ');
            console.info(colorJson(otherViolations));
        }

        if (seriousViolations.length > 0) {
            hasSeriousViolations = true;
        }

        console.log('\n');
    }

    await page.close();
    await browser.close();

    process.exit(hasSeriousViolations ? 1 : 0);
})();

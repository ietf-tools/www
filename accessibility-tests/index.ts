const { AxePuppeteer } = require('@axe-core/puppeteer');
const puppeteer = require('puppeteer');
const colorJson = require('color-json');

const baseUrl = process.argv[2]; // use the first argument

const testPaths = ['/', '/blog/'];

(async () => {
    console.log(`Testing ${baseUrl}`);
    const browser = await puppeteer.launch({
        args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });
    const page = await browser.newPage();
    if (process.env.BASIC_AUTH) {
        console.log('Basic auth set');
        await page.setExtraHTTPHeaders({
            // expects it to be already base64 encoded
            Authorization: `Basic ${process.env.BASIC_AUTH}`,
        });
    }
    await page.setBypassCSP(true);
    let hasSeriousViolations = false;

    try {
        for (let i = 0; i < testPaths.length; i++) {
            const testPath = testPaths[i];
            const url = new URL(testPath, baseUrl).toString();

            await page.goto(url), { waitUntil: 'networkidle0' };
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
    } catch (err) {
        console.error(err);
        hasSeriousViolations = true;
    }

    process.exit(hasSeriousViolations ? 1 : 0);
})();

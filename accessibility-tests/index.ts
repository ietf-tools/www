// This applies automated accessibility testing via Axe.
// See docs at
// https://www.npmjs.com/package/@axe-core/puppeteer

const { AxePuppeteer } = require('@axe-core/puppeteer');
const puppeteer = require('puppeteer');
const colorJson = require('color-json');

const baseUrl = process.argv[2]; // use the first argument

const testPaths = [
    '/',
    '/calintest-homepage-1/calin-topic-page-list/', 
    '/calintest-homepage-1/calintest-topic-page1/',
    '/calintest-homepage-1/calintest-topic-page-empty/',
    '/calintest-homepage-1/calintest-standard-page/',
    '/calintest-homepage-1/calintest-standard-page-empty/',
    '/calintest-homepage-1/calintest-index-page-1/',
    '/calintest-homepage-1/calintest-index-page-empty/',
    '/calintest-homepage-1/calintest-iesg-statements-index-page/',
    '/calintest-homepage-1/calintest-glossary-page-1/',
    '/calintest-homepage-1/calintest-glossary-page-empty/',
    '/calintest-homepage-1/calintest-form-page-1/',
    '/calintest-homepage-1/calintest-form-page-empty/',
    '/calintest-homepage-1/calintest-event-page-1/',
    '/calintest-homepage-1/calintest-event-page-empty/',
    '/calintest-homepage-1/calintest-event-listing-page-max1/',
    '/calintest-homepage-1/calintest-event-listing-empty/',
    '/calintest-homepage-1/calintest-event-listing-page-1/',
    '/calintest-homepage-1/titletitletitletitletitletitletitletitletitletitle/',
    '/calintest-homepage-1/calintest-homepage/',
];

const violationImpactsThatFail = ['serious', 'critical'];

// Add rules to disable here. Be careful to only disable errors that are false positives!
const rulesToDisable: string[] = [];

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
    let hasViolationsThatFail = false;

    try {
        for (let i = 0; i < testPaths.length; i++) {
            const testPath = testPaths[i];
            const url = new URL(testPath, baseUrl).toString();
            console.log(`Testing URL: ${url}`);
            await page.goto(url), { waitUntil: 'networkidle0' };
            const allResults = await new AxePuppeteer(page)
                .disableRules(rulesToDisable)
                .analyze();
            const failTestViolations = allResults.violations.filter(
                (violation: any) =>
                    violationImpactsThatFail.includes(violation.impact),
            );

            const warningTestViolations = allResults.violations.filter(
                (violation: any) =>
                    violationImpactsThatFail.includes(violation.impact) ===
                    false,
            );

            if (
                failTestViolations.length > 0 ||
                warningTestViolations.length > 0
            ) {
                console.log(`Testing ${url} found violations`);
            } else {
                console.log(`No violations at ${url}`);
            }

            if (failTestViolations.length > 0) {
                console.error(colorJson(failTestViolations));
            }

            if (warningTestViolations.length > 0) {
                console.info('Other violations: ');
                console.info(colorJson(warningTestViolations));
            }

            if (failTestViolations.length > 0) {
                hasViolationsThatFail = true;
            }

            console.log('\n');
        }

        await page.close();
        await browser.close();
    } catch (err) {
        console.error(err);
        hasViolationsThatFail = true;
    }

    process.exit(hasViolationsThatFail ? 1 : 0);
})();

/**
 * Playwright Test Orchestration with Coverage & User Analytics
 *
 * Steps:
 * 1. Load test mapping (with usage scores), flaky tracker, and simulated coverage.
 * 2. Map changed files to relevant tests.
 * 3. Prioritize tests by feature order, coverage gaps, and user behavior.
 * 4. Filter out flaky tests (retryCount > 1).
 * 5. Log selected tests and those improving coverage.
 * 6. Run selected tests using Playwright CLI.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Utility: Load JSON file
function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

// Step 1: Load mapping, flaky tracker, and simulated coverage
const mappingPath = path.join(__dirname, '.vscode', 'test_mapping.json');
const flakyPath = path.join(__dirname, '.vscode', 'flaky_tracker.json');

// --- Simulate coverage-summary.json ---
const coverageSummary = {
  "trip.test.js": { pct: 60 },      // Under-tested
  "map.test.js": { pct: 85 },       // Well-tested
  "login.test.js": { pct: 50 },     // Under-tested
  "flaky.test.js": { pct: 90 }      // Well-tested
};

// --- Load test mapping and flaky tracker ---
const testMappingRaw = loadJson(mappingPath).feature;
const flakyTracker = loadJson(flakyPath);

// --- Simulate usage scores inside test-mapping.json structure ---
const testMapping = {};
for (const [feature, details] of Object.entries(testMappingRaw)) {
  // Add usageScore to each feature (simulate: Trip purpose=0.9, Live Location=0.7)
  testMapping[feature] = {
    ...details,
    usageScore: feature === "Trip purpose" ? 0.9 :
                feature === "Live Location" ? 0.7 : 0.5
  };
}

// Step 2: Simulate changed files (replace with git diff or watcher in real use)
const changedFiles = [
  'start_trip.js',
  'login.js',
  'flaky.js'
];

// Step 3a: Map changed files to tests
function mapChangedFilesToTests(changedFiles, testMapping) {
  const selectedTests = new Set();

  for (const [feature, details] of Object.entries(testMapping)) {
    // APIs
    if (details.api) {
      for (const api of details.api) {
        if (changedFiles.some(f => f.includes(api.replace('/', '')))) {
          (details.tests || details.teste || []).forEach(test => selectedTests.add(test));
        }
      }
    }
    // UI
    if (details.ui) {
      for (const uiElem of details.ui) {
        if (changedFiles.some(f => f.includes(uiElem.replace('#', '')))) {
          (details.tests || details.teste || []).forEach(test => selectedTests.add(test));
        }
      }
    }
  }
  // Always include login and flaky tests if changed
  if (changedFiles.some(f => f.includes('login'))) selectedTests.add('login.test.js');
  if (changedFiles.some(f => f.includes('flaky'))) selectedTests.add('flaky.test.js');

  return Array.from(selectedTests);
}

// Step 3b: Coverage-aware prioritization
function getCoverageForTest(testFile, coverageSummary) {
  return coverageSummary[testFile]?.pct ?? 0;
}

function getCoverageGapTests(tests, coverageSummary, threshold = 80) {
  // Select tests covering files below threshold
  return tests.filter(test => getCoverageForTest(test, coverageSummary) < threshold);
}

// Step 3c: User analytics prioritization
function getUsageScore(testFile, testMapping) {
  for (const [feature, details] of Object.entries(testMapping)) {
    if ((details.tests || details.teste || []).includes(testFile)) {
      return details.usageScore ?? 0.5; // Default medium score
    }
  }
  return 0.5;
}

function prioritizeTests(tests, testMapping, coverageSummary) {
  const priorityOrder = Object.keys(testMapping);
  return tests.sort((a, b) => {
    // Feature order
    const aFeature = priorityOrder.find(feature => (testMapping[feature].tests || testMapping[feature].teste || []).includes(a));
    const bFeature = priorityOrder.find(feature => (testMapping[feature].tests || testMapping[feature].teste || []).includes(b));
    const featureCmp = priorityOrder.indexOf(aFeature || '') - priorityOrder.indexOf(bFeature || '');
    if (featureCmp !== 0) return featureCmp;

    // Coverage gap (lower coverage = higher priority)
    const aCov = getCoverageForTest(a, coverageSummary);
    const bCov = getCoverageForTest(b, coverageSummary);
    if (aCov !== bCov) return aCov - bCov;

    // User analytics (higher usage = higher priority)
    const aScore = getUsageScore(a, testMapping);
    const bScore = getUsageScore(b, testMapping);
    return bScore - aScore;
  });
}

// Step 4: Filter out flaky tests (retryCount > 1)
function filterFlakyTests(tests, flakyTracker) {
  return tests.filter(test => !(flakyTracker[test] && flakyTracker[test].retryCount > 1));
}

// Step 5: Run selected tests using Playwright CLI
function runPlaywrightTests(testFiles) {
  if (testFiles.length === 0) {
    console.log('No relevant Playwright tests found for the changed files.');
    return;
  }
  console.log('Selected Playwright tests:', testFiles);

  // Build CLI command
  const testPaths = testFiles.map(f => `"tests/${f}"`).join(' ');
  const cmd = `npx playwright test ${testPaths} --coverage`;
  console.log(`Running: ${cmd}`);
  try {
    execSync(cmd, { stdio: 'inherit' });
  } catch (err) {
    console.error('Test run failed:', err.message);
  }
}

// Orchestration main
function main() {
  let tests = mapChangedFilesToTests(changedFiles, testMapping);
  // Coverage gap tests (untested/under-tested)
  const coverageGapTests = getCoverageGapTests(tests, coverageSummary);
  if (coverageGapTests.length > 0) {
    console.log('Tests that improve coverage:', coverageGapTests);
  }
  // Prioritize by feature, coverage, and user analytics
  tests = prioritizeTests(tests, testMapping, coverageSummary);
  tests = filterFlakyTests(tests, flakyTracker);
  runPlaywrightTests(tests);
}

main();

/**
 * Coverage Influence:
 * - Tests covering files with <80% coverage are prioritized.
 * - Outputs list of tests that improve coverage.
 *
 * User Analytics Influence:
 * - Features with higher usage scores (from mapping) are prioritized.
 * - Usage scores are simulated in test-mapping.json structure.
 *
 * All logic is modular and paths are dynamically*/
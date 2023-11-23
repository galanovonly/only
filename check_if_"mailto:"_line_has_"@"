pm.test('Check responseBody', function () {
    var responseBody = pm.response.text();

    // Find all occurrences of "mailto:"
    var mailtoMatches = responseBody.match(/mailto:.*?"/g);

    // If "mailto:" is present, check if "@" is in the same line for each occurrence
    if (mailtoMatches) {
        for (const mailtoMatch of mailtoMatches) {
            // Test failed if "mailto:" line doesn't contain "@"
            pm.expect(mailtoMatch.includes('@')).to.be.true;
        }
    } else {
        // Test passed if "mailto:" is not present
        pm.expect(true).to.be.true;
    }
});

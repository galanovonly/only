pm.test("Short Link Check", function () {
    var responseBody = pm.response.text();
    var secondColumnURL = pm.iterationData.get("...ColumnNameWithIncorrectLinkFromCSV...") + "\"";
    var thirdColumnURL = pm.iterationData.get("...ColumnNameWithCorrectLinkFromCSV") + "\"";

    // Check if secondColumnURL is equal to thirdColumnURL and if thirdColumnURL is in responseBody or if thirdColumnURL includes "/media/archive" and if thirdColumnURL is in responseBody
    if (secondColumnURL === thirdColumnURL && responseBody.includes(thirdColumnURL) || secondColumnURL.slice(0, -1) === thirdColumnURL.slice(0, -1) && responseBody.includes(thirdColumnURL.slice(0, -1)) || secondColumnURL === thirdColumnURL && thirdColumnURL.includes("/media/archive")) {
        // Test is passed
        pm.expect(true).to.be.true;
    } else if (secondColumnURL !== thirdColumnURL) {
        // Check if thirdColumnURL has "/rus" at the beginning
        if (thirdColumnURL.startsWith("/rus") && !secondColumnURL.startsWith("/eng") && !secondColumnURL.startsWith("/rus")) {
            // Add "/rus" to the beginning of secondColumnURL
            secondColumnURL = "/rus" + secondColumnURL;

            // Check if secondColumnURL is equal to thirdColumnURL and if thirdColumnURL is in responseBody
            if (secondColumnURL === thirdColumnURL && responseBody.includes(thirdColumnURL) || secondColumnURL.slice(0, -1) + "/\"" === thirdColumnURL && responseBody.includes(thirdColumnURL) || thirdColumnURL.includes("/media/archive")) {
                // Test is passed
                pm.expect(true).to.be.true;
            } else {
                // Test is failed
                pm.expect(false, "+/rus false").to.be.true;
            }
        } else {
            // Check if thirdColumnURL is in responseBody
            if (responseBody.includes(thirdColumnURL) && !responseBody.includes(secondColumnURL) || secondColumnURL.slice(0, -1) + "/\"" === thirdColumnURL && responseBody.includes(thirdColumnURL)) {
                // Test is passed
                pm.expect(true).to.be.true;
            } else {
                // Test is failed
                pm.expect(false, "thirdColumnURL is not in responseBody or secondColumnURL is found in responseBody").to.be.true;
            }
        }
    } else {
        // Test is failed
        pm.expect(false, "no/rus false").to.be.true;
    }
});

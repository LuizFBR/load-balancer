function ExponentialDistribution(){
}

ExponentialDistribution.getRandomExponential = function (lambda) {
    // Generate a uniformly distributed random number between 0 and 1
    let u = Math.random()
    // Apply inverse transform sampling to generate an exponentially distributed value
    return Math.round(-Math.log(1 - u) / lambda)
}
  
ExponentialDistribution.generateExponentialSample = function (min, max, lambda, sampleSize) {
    let samples = [];
    for (let i = 0; i < sampleSize; i++) {
        let expSample;
        do {
        // Generate a random exponential sample, round to nearest integer
        expSample = Math.round(ExponentialDistribution.getRandomExponential(lambda));
        } while (expSample < min || expSample > max); // Ensure it's within the range
        samples.push(expSample);
    }
    return samples;
}

module.exports = {ExponentialDistribution};
  
// // Example usage:
// let min = 1;
// let max = 65e3; // Max TCP packet size
// let lambda = 0.001;  // mean value is 1/lambda = 10000
// let numberOfRequisitions = ExponentialDistribution.getRandomExponential(1e-6) // receives on average 1e6 requisitions per second.

// let samples = ExponentialDistribution.generateExponentialSample(min, max, lambda, numberOfRequisitions);
// console.log(samples);
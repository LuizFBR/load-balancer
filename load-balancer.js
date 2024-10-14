const { ExponentialDistribution } = require('./sample.js');

const { randomInt } = require('crypto'); // Use built-in Node.js module for randomness
const fs = require('fs');
const { file_system } = require('./file-system.js');

function generateOrderedList(n, start, end) {
    // Generate 'n' random unique integers in the range [start, end]
    const randomIntegers = new Set();
    while (randomIntegers.size < n) {
        randomIntegers.add(randomInt(start, end + 1));
    }

    // Convert Set to Array and sort it to ensure it's ordered
    return Array.from(randomIntegers).sort((a, b) => a - b);
}

function processorTypes() {
    this.processors = [
        Intel_Core_i7_8700K =
        {
            base_frequency: "4.7 GHz",
            base_frequency_number: 4.7e3, // diminuindo algumas magnitudes
            url: "https://ark.intel.com/content/www/us/en/ark/products/126684/intel-core-i7-8700k-processor-12m-cache-up-to-4-70-ghz.html",
        },
        Intel_Xeon_Platinum_8380 =
        {
            base_frequency: "2.30 GHz",
            base_frequency_number: 3.0e3, // diminuindo algumas magnitudes
            url: "https://www.intel.com.br/content/www/br/pt/products/sku/212287/intel-xeon-platinum-8380-processor-60m-cache-2-30-ghz/specifications.html",
        },
        Intel_Core_i9_12900K =
        {
            base_frequency: "2.40 GHz",
            base_frequency_number: 2.4e3, // diminuindo algumas magnitudes
            url: "https://www.intel.com.br/content/www/br/pt/products/sku/134599/intel-core-i912900k-processor-30m-cache-up-to-5-20-ghz/specifications.html",
        },
    ]
}

function createRequest(requestId, percentage, packetSize, cycle) {
    return {
        id: requestId,
        type: percentage, // percentage of the requisition that consists of I/O operations.
        size: packetSize,
        loadReceiveTime: cycle,
    }
};

function trafficSimulator() {
    const NUMBER_OF_CYCLES = 1e2; // minimum number of cycles

    const cycles = generateOrderedList(NUMBER_OF_CYCLES, 0, NUMBER_OF_CYCLES);
    const traffic = {};

    // Example usage:
    const min = 1;
    const max = 65e3; // Max TCP packet size
    const lambda = 0.001;  // mean value of packet size is 1/0.001 = 1000
    const numberOfRequisitions = ExponentialDistribution.getRandomExponential(1e-2) // receives on average 10000 requisitions per second.
    let requestId = 0;
    for (let cycle of cycles) {
        const reqs = [];
        exponentialDistributionSizeSample = ExponentialDistribution.generateExponentialSample(min, max, lambda, numberOfRequisitions)
        for (let i = 0; i < numberOfRequisitions; i++) {
            reqs.push(createRequest(requestId++, Math.random(), exponentialDistributionSizeSample[i], cycle)); // req can be I/O or processing (0 or 1)
        }
        traffic[cycle] = reqs;
    }

    return traffic;
}

class ServerSimulator {
    static cycle = 0;

    constructor(processor) {
        // Suponha que 1 ciclo consegue processar até 32 bits/4bytes.
        this.bytesProcessedPerCycle = processor['base_frequency_number'] * 4
        this.queue = [];
    }

    receiveLoad(load) {
        this.queue.push(load);
        // console.log(`receive load: ${JSON.stringify(load)}`)
    }
    processLoad() { // returns number of completely processed packages
        let throughput = 0;
        let finishedPacketsIds = []
        let first = this.queue[0];
        let totalBytesLeftPerDelta = this.bytesProcessedPerCycle
        while (this.queue.length > 0 && totalBytesLeftPerDelta > 0) {
            let first = this.queue[0];
            let processing_size =  3*first.size*first.type + 2*first.size*(1-first.type); // Operações I/O tomam 3* o tempo e de processamento tomam 2* o tempo
            // console.log(`para processar ${JSON.stringify(first)} bytes faltantes: ${processing_size} capacidade restante: ${totalBytesLeftPerDelta } \n`);
            if (processing_size <= totalBytesLeftPerDelta) { // if total load can be processed
                this.queue.shift(); // Remove the first element
                // console.log(`Finish processing packet ${JSON.stringify(first)}\n on cycle ${ServerSimulator.cycle}`);
                totalBytesLeftPerDelta -= processing_size;
                throughput++; //counts each processed packet
                finishedPacketsIds.push(first.id)
            }
            else { // processing_Time > totalBytesLeftPerDelta
                first.size -= totalBytesLeftPerDelta/(3*first.type) + totalBytesLeftPerDelta/(2*(1-first.type)); // packet remembers the amount of bytes left to be processed.
                totalBytesLeftPerDelta = 0;
            }
        }
        return [throughput, finishedPacketsIds]
    }
    cleanQueue() {
        this.queue = []
    }
}

function random_queue_selection_policy(servers) {
    return randomInt(0, servers.length)
}

function round_robin_selection_policy() {
    let count = 0; // This variable is private and persists across calls

    return function (servers) {
        count = count % servers.length
        return count++;
    };
}

function shortest_queue_selection_policy(servers) {
    let min_queue = Number.MAX_SAFE_INTEGER
    let index = 0
    for (i = 0; i < servers.length; i++) {
        if (servers[i].queue.length < min_queue) {
            min_queue = servers[i].queue.length
            index = i
        }
    }
    return index
}

function LoadBalancer(load_balancing_policy, servers) {
    this.policy = load_balancing_policy
    this.servers = servers

    this.balanceLoad = function (load) {
        let index = this.policy(servers)
        servers[index].receiveLoad(load)
        return index + 1 // returns server id
    }
}

class TestSimulator {
    constructor(loadBalancer) {
        this.loadBalancer = loadBalancer;
        this.throughput = 0;
        this.responseTimes = {}
    }

    beginSimulation(traffic, servers) {
        let log = {}
        while (ServerSimulator.cycle <= Math.max(...Object.keys(traffic))) { // Simulate until a certain cycle value
            log[ServerSimulator.cycle] = {}
            console.log(ServerSimulator.cycle);

            if (ServerSimulator.cycle in traffic) {
                traffic[ServerSimulator.cycle].forEach(load => {
                    let sId = this.loadBalancer.balanceLoad(load); // returns the selected server by the LoadBalancer.
                    log[ServerSimulator.cycle][load.id] = sId; // logs which server the load went to.
                    this.responseTimes[load.id] = {};
                    this.responseTimes[load.id].cycle_received = ServerSimulator.cycle;
                    this.responseTimes[load.id].cycle_finished_processing = Object.keys(traffic).length; // if this load never finishes processing, then it has the default cycle which it has finished processing as the final cycle.
                });
            }
            for (let server of servers) {
                let cycleThroughput, cycleProcessedIds;
                [cycleThroughput, cycleProcessedIds] = server.processLoad();
                this.throughput += cycleThroughput;
                for (let id of cycleProcessedIds)
                    this.responseTimes[id].cycle_finished_processing = ServerSimulator.cycle;
            }
            ServerSimulator.cycle += 1;
        }
        ServerSimulator.cycle = 0; // resets the simulation cycle.
        return log;
    }
}

function generateTrafficInstances() {
    for (let i = 0; i < 1e3; i++) {
        traffic = trafficSimulator()
        file_path = `traffic/traffic${i}.json`
        file_system.writeObjToFile(traffic, file_path)
        console.log(`finished generating and writing traffic${i}.json on traffic folder`)
    }
}

generateTrafficInstances();

processors = new processorTypes().processors;

const s1 = new ServerSimulator(processors[0]);
const s2 = new ServerSimulator(processors[1]);
const s3 = new ServerSimulator(processors[2]);

const rqLoadBalancer = new LoadBalancer(random_queue_selection_policy, [s1, s2, s3])
const rrLoadBalancer = new LoadBalancer(round_robin_selection_policy(), [s1, s2, s3])
const sqLoadBalancer = new LoadBalancer(shortest_queue_selection_policy, [s1, s2, s3])

// execute all random queue tests
for (let i = 0; i < 1e3 ; i++) {
    traffic = file_system.readObjFromFile(`traffic/traffic${i}.json`);
    console.log(`////////////////\n\nBeggining random queue test on traffic ${i} \n\n////////////////`);
    test = new TestSimulator(rqLoadBalancer);
    log = test.beginSimulation(traffic, [s1, s2, s3]);
    log.throughput = test.throughput / Object.keys(test.responseTimes).length;
    log.avg_response_time = Object.keys(test.responseTimes).reduce(
        (accumulator, reponse_times) => accumulator + (
            test.responseTimes[reponse_times].cycle_finished_processing - test.responseTimes[reponse_times].cycle_received),
        0,
    ) / Object.keys(test.responseTimes).length;
    file_system.writeObjToFile(log, `log/rqLoadBalancerLogTraffic${i}.json`);
    // Cleans servers queue for next test
    s1.cleanQueue();
    s2.cleanQueue();
    s3.cleanQueue();
}

// execute all round robin tests
    for (let i = 0; i < 1e3; i++) {
    console.log(`////////////////\n\nBeggining round robin test on traffic ${i} \n\n////////////////`);
    traffic = file_system.readObjFromFile(`traffic/traffic${i}.json`);
    test = new TestSimulator(rrLoadBalancer);
    log = test.beginSimulation(traffic, [s1, s2, s3]);
    log.throughput = test.throughput / Object.keys(test.responseTimes).length;
    log.avg_response_time = Object.keys(test.responseTimes).reduce(
        (accumulator, reponse_times) => accumulator + (
            test.responseTimes[reponse_times].cycle_finished_processing - test.responseTimes[reponse_times].cycle_received),
        0,
    ) / Object.keys(test.responseTimes).length;
    file_system.writeObjToFile(log, `log/rrLoadBalancerLogTraffic${i}.json`);
    // Cleans servers queue for next test
    s1.cleanQueue();
    s2.cleanQueue();
    s3.cleanQueue();
}

// // execute all shortest queue tests
for (let i = 0; i < 1e3; i++) {
    traffic = file_system.readObjFromFile(`traffic/traffic${i}.json`);
    console.log(`////////////////\n\nBeggining shortest queue test on traffic ${i} \n\n////////////////`);
    test = new TestSimulator(sqLoadBalancer);
    log = test.beginSimulation(traffic, [s1, s2, s3]);
    log.throughput = test.throughput / Object.keys(test.responseTimes).length;
    log.avg_response_time = Object.keys(test.responseTimes).reduce(
        (accumulator, reponse_times) => accumulator + (
            test.responseTimes[reponse_times].cycle_finished_processing - test.responseTimes[reponse_times].cycle_received),
        0,
    ) / Object.keys(test.responseTimes).length;
    file_system.writeObjToFile(log, `log/sqLoadBalancerLogTraffic${i}.json`);
    // Cleans servers queue for next test
    s1.cleanQueue();
    s2.cleanQueue();
    s3.cleanQueue();
}
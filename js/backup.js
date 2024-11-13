let isRunning = false;
let load = 10;
let workers = [];
let workerCount = 0;

google.charts.load('current', { packages: ['gauge'] });
google.charts.setOnLoadCallback(drawChart);

let data, chart, options;

function drawChart() {
    data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['CPU', load]
    ]);
    options = {
        width: 300, height: 160,
        redFrom: 90, redTo: 100,
        yellowFrom: 75, yellowTo: 90,
        greenFrom: 0, greenTo: 75,
        minorTicks: 5,
        max: 100
    };
    chart = new google.visualization.Gauge(document.getElementById('gauge_div'));
    chart.draw(data, options);
}

function updateGauge(value) {
    data.setValue(0, 1, value);
    chart.draw(data, options);
}

function toggleStressTest() {
    if (isRunning) {
        stopStressTest();
    } else {
        startStressTest();
    }
}

function startStressTest() {
    if (window.Worker) {
        workerCount = 0;
        let totalWorkers;
        if (load >= 1 && load <= 10) {
            totalWorkers = 8;
        } else if (load >= 11 && load <= 20) {
            totalWorkers = 16;
        } else if (load >= 21 && load <= 30) {
            totalWorkers = 24;
        } else if (load >= 31 && load <= 100) {
            totalWorkers = 50;
        }

        for (let i = 0; i < totalWorkers; i++) {
            const delay = load < 10 ? 200 - load * 10 : 50 - (load * 0.5);
            const worker = new Worker(URL.createObjectURL(new Blob([`
                setInterval(() => {
                    for (let i = 0; i < ${load * 5000}; i++) {
                        Math.sqrt(Math.random() * Math.random());
                    }
                    postMessage('load');
                }, ${delay});
            `], { type: 'application/javascript' })));

            worker.onmessage = () => {
                updateGauge(load);
            };

            workers.push(worker);
            workerCount++;
        }

        isRunning = true;
        document.getElementById('status').innerText = `Status: ${workerCount}-WK Stressing...`;
        document.getElementById('stressButton').innerText = 'Stop Stress Test';
    } else {
        alert("Your browser does not support Web Workers.");
    }
}

function stopStressTest() {
    workers.forEach(worker => worker.terminate());
    workers = [];
    workerCount = 0;
    isRunning = false;
    document.getElementById('status').innerText = 'Status: Stopped';
    document.getElementById('stressButton').innerText = 'Start Stress Test';
    updateGauge(0);
}

function adjustLoad(value) {
    load = value;
    document.getElementById('loadDisplay').innerText = value;
    updateGauge(load);
    if (isRunning) {
        stopStressTest();
        startStressTest();
    }
}

function increaseLoad() {
    if (load < 100) {
        load++;
        document.getElementById('loadSlider').value = load;
        adjustLoad(load);
    }
}

function decreaseLoad() {
    if (load > 1) {
        load--;
        document.getElementById('loadSlider').value = load;
        adjustLoad(load);
    }
}
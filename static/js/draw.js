var mappedData;
function prepareChartData(jsonData, prop) {
    mappedData = {};
    getRandomNumber = () => {
        return Math.floor(Math.random() * 256);
    }

    jsonData.forEach(element => {
        var md = mappedData[element[prop]];
        if (!md) mappedData[element[prop]] = md = { count: 0, elements: [] };
        md.count++;
        md.elements.push(element);
        md.color = `${getRandomNumber()}, ${getRandomNumber()}, ${getRandomNumber()}`;
    });

    return {
        labels: Object.keys(mappedData),
        datasets: [{
            label: 'count by ' + prop,
            data: Object.keys(mappedData).map((key) => mappedData[key].count),
            backgroundColor: Object.keys(mappedData).map((key) => `rgba(${mappedData[key].color}, 0.3)`),
            borderColor: Object.keys(mappedData).map((key) => `rgb(${mappedData[key].color})`),
            borderWidth: 1
        }]
    }
}

function prepareOptions(data) {
    return {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            events: ['click']
        }
    }
}

function initChart(options, elemId) {
    const canvas = document.getElementById(elemId);
    var myChart = new Chart(canvas, options);
    canvas.onclick = (evt) => {

        const activePoints = myChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

        if (activePoints.length > 0) {
            // Get the dataset index and data index of the clicked point
            const datasetIndex = activePoints[0].datasetIndex;
            const dataIndex = activePoints[0].index;

            // Get the clicked bar data and label
            const clickedData = myChart.data.datasets[datasetIndex].data[dataIndex];
            const clickedLabel = myChart.data.labels[dataIndex];

        }
    }
    return myChart;
}

var chart,
    data = {};
function draw(context, chartElementId, checkboxId) {
    var prop = document.getElementById(checkboxId).checked ? "temperament" : "category";

    if (!data[prop])
        data[prop] = prepareChartData(JSON.parse(context), prop);
    if (chart) {
        chart.data = data[prop];
        chart.update();
    }
    else
        chart = initChart(prepareOptions(data[prop]), chartElementId)
};
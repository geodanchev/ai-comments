const chartData = {};

function getRandomNumber() {
    return Math.floor(Math.random() * 256);
}

function prepareChartData(jsonData, toggle) {
    const prop = toggle.checked ? "temperament" : "category";

    if (chartData[prop]) return chartData[prop];

    chartData[prop] = {};

    jsonData.forEach(element => {
        const key = element[prop];
        if (!chartData[prop][key]) {
            chartData[prop][key] = {
                count: 0,
                elements: [],
                color: `${getRandomNumber()}, ${getRandomNumber()}, ${getRandomNumber()}`
            };
        }
        chartData[prop][key].count++;
        chartData[prop][key].elements.push(element);
    });

    return chartData[prop];
}

function init(jsonData, chartElementId, checkboxId) {
    const toggle = document.getElementById(checkboxId),
        data = JSON.parse(jsonData),
        chart = new DrawChart(chartElementId, prepareChartData(data, toggle));

    toggle.onclick = () => chart.update(prepareChartData(data, toggle));
}
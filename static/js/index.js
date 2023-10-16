class DrawChart {
    constructor(canvasId, mappedData) {
        const canvas = document.getElementById(canvasId);
        canvas.onclick = this.#canvasClicked;
        this.myChart = new Chart(canvas, this.#getOptions(this.#buildData(mappedData)));
        this.mappedData = mappedData;
    }
    update(newMappedData) {
        this.mappedData = newMappedData;
        this.myChart.data = newMappedData;
        this.myChart.update();
    }
    #getOptions(data) {
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
    #buildData(mappedData) {
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
    #canvasClicked(evt) {
        const activePoints = this.myChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

        if (activePoints.length > 0) {
            const dataIndex = activePoints[0].index;
            const clickedLabel = this.myChart.data.labels[dataIndex];
            console.log(this.mappedData[clickedLabel]);
        }
    }
}
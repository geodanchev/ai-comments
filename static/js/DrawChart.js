class DrawChart {
    constructor(canvasId, mappedData) {
        const canvas = document.getElementById(canvasId);
        canvas.onclick = this.#canvasClicked.bind(this);
        this.myChart = new Chart(canvas, this.#getOptions(this.#buildData(mappedData)));
        this.mappedData = mappedData;
    }
    update(newMappedData) {
        this.mappedData = newMappedData;
        this.myChart.data = this.#buildData(newMappedData);
        this.myChart.update();
    }
    #getOptions(data) {
        return {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Customer feedback'
                    }
                }
            },
        };
    }
    #buildData(mappedData) {
        return {
            labels: Object.keys(mappedData),

            datasets: [{
                label: 'count by ', //+ prop,
                data: Object.keys(mappedData).map((key) => mappedData[key].count),
                backgroundColor: Object.keys(mappedData).map((key) => `rgba(${mappedData[key].color})`),
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
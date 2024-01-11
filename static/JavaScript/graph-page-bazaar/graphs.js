function create_chart(data1, data2, data3, values, ctx){

    new Chart(ctx, {
    type: "line",
    data: {
    labels: values,
    datasets: [{
            data: data1,
            borderColor: "#008FFB",
            fill: true,
            label: "buy",
            backgroundColor: '#385164',
        },
        {
            data: data2,
            borderColor: "#00E396",
            fill: true,
            label: "sell",
            backgroundColor: '#386052',
        },
        {
            data: data3,
            borderColor: "#f1d460",
            label: "avg buy price",
            backgroundColor: "#877536"
        }
        ]
    },
    options: {

        legend: {display: true},
        scales: {
            xAxes: [{
            display: true,
            gridLines: {
                display: false
            },
            ticks : {
                fontColor : "#FFFFFF"
            }
            }],
            yAxes: [{
            display: true,
            gridLines: {
                display: false,
            },
            ticks : {
                fontColor : "#FFFFFF"
            }
            }]
        }
    }
    });
}

function toUpperCaseWithUnderscores(str) {
    return str.toUpperCase().split(' ').join('_');
}

const item = toUpperCaseWithUnderscores(document.querySelector("h1").textContent)
console.log(item)

axios.get(`http://chalumoid.fr/projects/bazaar-tracker/items/${item}/api`)
    .then(function (response) {
        console.log(response.data);
        const graphDatas = response.data
        for (let i = 0; i < graphDatas.graphAmount; i++) {
            create_chart(graphDatas.graphDatas[i][0], graphDatas.graphDatas[i][1], graphDatas.graphDatas[i][2], graphDatas.graphBottomData[i], document.querySelector("#graph"))
        }
    })
    .catch(function (error) {
        // en cas d’échec de la requête
        console.log(error);
        const canva = document.querySelector("#graph");
        const wrapper = document.createElement("a");
        wrapper.id = "apiErrorText"
        canva.parentNode.insertBefore(wrapper, canva);
        wrapper.parentNode.style.height = "75%"
        canva.remove();
        wrapper.textContent = "Error loading data."
    })

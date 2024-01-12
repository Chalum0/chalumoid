const item = toUpperCaseWithUnderscores(document.querySelector("h1").textContent)
let amounts = JSON.parse(localStorage.getItem("amounts"))
console.log(amounts)
if (amounts === null) {
    amounts = {

    }
    amounts[item] = {values: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], bottomValues: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
}



const buyButton = document.querySelector("#buy-button")
const sellButton = document.querySelector("#sell-button")
function canBeConvertedToInt(str) {
    let num = parseInt(str);
    return !isNaN(num);

}

buyButton.addEventListener("click", ()=>{
    let amount = document.querySelector("#quantity").value
    if (amount !== "" && canBeConvertedToInt(amount)){
        amounts[item].values.push(
            parseFloat(amounts[item].values[amounts[item].values.length - 1]) + parseFloat(amount)
        )
        amounts[item].values.shift()
        createChart(amounts[item].values, amounts[item].bottomValues, "Stock", document.querySelector("#graph2"))
        localStorage.setItem("amounts", JSON.stringify(amounts))
    }
})

sellButton.addEventListener("click", ()=>{
    let amount = document.querySelector("#quantity").value
    if (amount !== "" && canBeConvertedToInt(amount)){
        amounts[item].values.push(
            parseFloat(amounts[item].values[amounts[item].values.length - 1]) - parseFloat(amount)
        )
        amounts[item].values.shift()
        createChart(amounts[item].values, amounts[item].bottomValues, "Stock", document.querySelector("#graph2"))
        localStorage.setItem("amounts", JSON.stringify(amounts))
    }
})

// localStorage.setItem("amounts", JSON.stringify(amounts))



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

function createChart(data, values, label, ctx){
    new Chart(ctx, {
        type: "line",
        data: {
            labels: values,
            datasets: [{
                data: data,
                borderColor: "#008FFB",
                fill: false,
                label: label,
                backgroundColor: '#385164',
            }
            ]
        },
        options: {

            legend: {display: true},
            scales: {
                xAxes: [{
                    display: false,
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

createChart(amounts[item].values, amounts[item].bottomValues, "Stock", document.querySelector("#graph2"))


function talkToAPI(){
    axios.get(`http://chalumoid.fr/projects/bazaar-tracker/items/${item}/api`)
        .then(function (response) {
            const apiData = response.data

            // --CREATE GRAPH FROM API DATA
            let graphData = apiData //apiData.graph
            create_chart(graphData.graphDatas[0][0], graphData.graphDatas[0][1], graphData.graphDatas[0][2], graphData.graphBottomData[0], document.querySelector("#graph"))



            // --CREATE TABLE FROM API DATA
            // const table = document.querySelector("table")
            // let tableData = apiData.table
            // for (let v of tableData.buy) {
            //     let td1 = document.createElement("td")
            //     td1.textContent = v[0]
            //     let td2 = document.createElement("td")
            //     td2.textContent = v[1]
            //
            //     table.appendChild(document.createElement("tr").appendChild(td1).appendChild(td2))
            // }




        })
        .catch(function (error) {
            // en cas d’échec de la requête
            console.log(error);
            const canva = document.querySelector("#graph");
            const wrapper = document.createElement("a");
            wrapper.className = "apiErrorText"
            canva.parentNode.insertBefore(wrapper, canva);
            wrapper.parentNode.style.height = "75%"
            canva.remove();
            wrapper.textContent = "Error loading data."

            const insideDiv = document.querySelector("#bottom-right-div>div")
            const wrapper2 = document.createElement("a")
            while (insideDiv.firstChild) {
                insideDiv.removeChild(insideDiv.firstChild);
            }
            wrapper2.className = "apiErrorText"
            insideDiv.appendChild(wrapper2)
            wrapper2.parentNode.style.height = "75%"
            wrapper2.textContent = "Error loading data."
        })
}

talkToAPI()
setInterval(talkToAPI(), 30*60*1000)


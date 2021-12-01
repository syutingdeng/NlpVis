

// var margin = { top: 10, right: 30, bottom: 30, left: 60 },
//     width = 460 - margin.left - margin.right,
//     height = 400 - margin.top - margin.bottom;


// var svg0 = d3.select("#my_dataviz")
//     .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//     .append("g")
//     .attr("transform",
//         "translate(" + margin.left + "," + margin.top + ")");


// function draw_scatter(data, layer, r) {
    
//     svg0.selectAll("g").remove()


//     var x = d3.scaleLinear()
//         .domain([0, 1])
//         .range([0, width]);
//     var xAxis = svg0.append("g")
//         .attr("transform", "translate(0," + height + ")")
//         .call(d3.axisBottom(x));

//     // Add Y axis
//     var y = d3.scaleLinear()
//         .domain([0, 1])
//         .range([height, 0]);
//     var yAxis = svg0.append("g")
//         .call(d3.axisLeft(y));


//     // Add dots

//     var circle = svg0.append('g')
//     var circleG = svg0.append('g')
//         .selectAll("dot")
//         .data(data)
//         .enter()
//         .append("circle")
//         .attr("id", d => d.id)
//         .attr("cx", function (d) { return x(d[layer]['hidden'][0]); })
//         .attr("cy", function (d) { return y(d[layer]['hidden'][1]); })
//         .attr("r", r)
//         .style("fill", "#000000")



//     var tip = d3.tip()
//         .attr('class', 'd3-tip')
//         .html(d => d[4].layer);

//     circleG.on('mouseover', tip.show)
//         .on('mouseout', tip.hide);

//     circleG.call(tip);


//     //brush

//     var brush = d3.brush()
//         .extent([[0, 0], [width, height]])
//         .on("start", brushed)
//         .on("brush", brushed)
//         ;
//     circle.call(brush);

//     function brushed() {
//         var extent = d3.event.selection;
//         var select_data = [];
//         circleG
//             .classed("selected", function (d) {
//                 selected =
//                     x(d[0]) >= extent[0][0] &&
//                     x(d[0]) <= extent[1][0] &&
//                     y(d[1]) >= extent[0][1] &&
//                     y(d[1]) <= extent[1][1];
//                 if (selected) {
//                     select_data.push(d);
//                 }
//                 //console.log("vis", select_data);
//                 return selected;
//             });


//     }

//     //console.log(rawData);
//     //console.log("td", tmp);

// }


function draw_scatter_zoom(data) {
    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // append the SVG object to the body of the page
    var SVG = d3.select("#dataviz_axisZoom")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear()
        .domain([0, 1])
        .range([0, width]);
    var xAxis = SVG.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    var yAxis = SVG.append("g")
        .call(d3.axisLeft(y));

    // Add a clipPath: everything out of this area won't be drawn.
    var clip = SVG.append("defs").append("SVG:clipPath")
        .attr("id", "clip")
        .append("SVG:rect")
        .attr("width", width)
        .attr("height", height)
        .attr("x", 0)
        .attr("y", 0);

    // Create the scatter variable: where both the circles and the brush take place

    var scatter = SVG.append('g')
        .attr("clip-path", "url(#clip)")

    // Add circles
    scatter
        .selectAll("circle")
        .data(data.result)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d[0]); })
        .attr("cy", function (d) { return y(d[1]); })
        .attr("r", 3)
        .attr("id", d => d[3])
        .attr("layer", d => d[4].layer)
        .style("fill", "#61a3a9")
        .style("opacity", 0.5)
        .style("fill", d => d[2])

    // Set the zoom and Pan features: how much you can zoom, on which part, and what to do when there is a zoom
    var zoom = d3.zoom()
        .scaleExtent([.5, 20])  // This control how much you can unzoom (x0.5) and zoom (x20)
        .extent([[0, 0], [width, height]])
        .on("zoom", updateChart);

    // This add an invisible rect on top of the chart area. This rect can recover pointer events: necessary to understand when the user zoom
    SVG.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .call(zoom);
    // now the user can zoom and it will trigger the function called updateChart

    // A function that updates the chart when the user zoom and thus new boundaries are available
    function updateChart() {

        // recover the new scale
        var newX = d3.event.transform.rescaleX(x);
        var newY = d3.event.transform.rescaleY(y);

        // update axes with these new boundaries
        xAxis.call(d3.axisBottom(newX))
        yAxis.call(d3.axisLeft(newY))

        // update circle position
        scatter
            .selectAll("circle")
            .attr('cx', function (d) { return newX(d[0]) })
            .attr('cy', function (d) { return newY(d[1]) });
    }




}

function draw_scatter_json(data, r) {

    var margin = { top: 10, right: 30, bottom: 30, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
    console.log(data)
    var SVG = d3.select("#my_dataviz6")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear()
        .domain([0, 1])
        .range([0, width]);
    var xAxis = SVG.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    var yAxis = SVG.append("g")
        .call(d3.axisLeft(y));


    // Add dots

    var circle = SVG.append('g')
    var circleG = SVG.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("id", d => d.word)
        .attr("cx", function (d) { return x(d.hidden[0]); })
        .attr("cy", function (d) { return y(d.hidden[1]); })
        .attr("r", r)
        .style("fill", d => d.color)



    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .html(d => d.word);

    circleG.on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    circleG.call(tip);


    //brush

    var brush = d3.brush()
        .extent([[0, 0], [width, height]])
        .on("start", brushed)
        .on("brush", brushed)
        ;
    circle.call(brush);

    function brushed() {
        var extent = d3.event.selection;
        var select_data = [];
        circleG
            .classed("selected", function (d) {
                selected =
                    x(d[0]) >= extent[0][0] &&
                    x(d[0]) <= extent[1][0] &&
                    y(d[1]) >= extent[0][1] &&
                    y(d[1]) <= extent[1][1];
                if (selected) {
                    select_data.push(d);
                }
                //console.log("vis", select_data);
                return selected;
            });


    }

    //console.log(rawData);
    //console.log("td", tmp);

}




var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz2")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

function drawLineChart(data) {
    console.log("d3", data)

    svg.selectAll("circle").remove()
    svg.selectAll("path").remove()

    var x = d3.scaleLinear()
        .domain([0, 12])
        .range([0, width]);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg.append("text")
        .attr("transform", `translate( ${width / 2} ,${height + 25} )`)
        .attr("font-size", "10px")
        .attr("text-anchor", "middle")
        .text("Accuracy")

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    var circle = svg.append('g')
    var circleG = svg.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d[1]); })
        .attr("cy", function (d) { return y(d[0]); })
        .attr("r", 5)



    // Add the line
    svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) { return x(d[1]) })
            .y(function (d) { return y(d[0]) })
        )

}





var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg2 = d3.select("#my_dataviz3")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

function drawScoreLineChart(data) {
    console.log("d3", data)

    svg2.selectAll("circle").remove()
    svg2.selectAll("path").remove()

    var x = d3.scaleLinear()
        .domain([0, 12])
        .range([0, width]);
    svg2.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    svg2.append("text")
        .attr("transform", `translate( ${width / 2} ,${height + 25} )`)
        .attr("font-size", "10px")
        .attr("text-anchor", "middle")
        .text("SoftMax_Score")


    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    svg2.append("g")
        .call(d3.axisLeft(y));

    var circle = svg2.append('g')
    var circleG = svg2.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d[1]); })
        .attr("cy", function (d) { return y(d[0]); })
        .attr("r", 5)



    // Add the line
    svg2.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) { return x(d[1]) })
            .y(function (d) { return y(d[0]) })
        )

}



var svg3 = d3.select("#my_dataviz4")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

function drawAttentionLineChart(data) {
    console.log("d3", data)

    svg3.selectAll("circle").remove()
    svg3.selectAll("path").remove()

    var x = d3.scaleLinear()
        .domain([0, 12])
        .range([0, width]);
    svg3.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
    svg3.append("text")
        .attr("transform", `translate( ${width / 2} ,${height + 25} )`)
        .attr("font-size", "10px")
        .attr("text-anchor", "middle")
        .text("Atteion to ClS")

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    svg3.append("g")
        .call(d3.axisLeft(y));

    var circle = svg3.append('g')
    var circleG = svg3.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d[1]); })
        .attr("cy", function (d) { return y(d[0]); })
        .attr("r", 5)



    // Add the line
    svg3.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
            .x(function (d) { return x(d[1]) })
            .y(function (d) { return y(d[0]) })
        )

}


function drawBarPlot(data, layer) {
    var margin = { top: 30, right: 30, bottom: 70, left: 60 },
        width = 460 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    sort_data = data.sort(function (x, y) {
        return d3.ascending(x.amount, y.amount)
    })
    console.log(sort_data)

    var x = d3.scaleBand()
        .range([0, width])
        .domain(sort_data.map(function (d) { return d.pos; }))
        .padding(0.2);
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, d3.max(sort_data, d => d.amount)])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // Bars
    svg.selectAll("mybar")
        .data(sort_data)
        .enter()
        .append("rect")
        .attr("x", function (d) { return x(d.pos); })
        .attr("y", function (d) { return y(d.amount); })
        .attr("width", x.bandwidth())
        .attr("height", function (d) { return height - y(d.amount); })
        .attr("fill", "#69b3a2")

}
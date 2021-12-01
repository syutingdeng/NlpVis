var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;


var svg0 = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

var x, y;
var circle, circleG;


function draw_scatter_cls(data, layer, r) {

    x = d3.scaleLinear()
        .domain([0, 1])
        .range([0, width]);
    var xAxis = svg0.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    y = d3.scaleLinear()
        .domain([0, 1])
        .range([height, 0]);
    var yAxis = svg0.append("g")
        .call(d3.axisLeft(y));

    circle = svg0.append('g')
    // Add dots
    circleG = svg0.append('g')
        .selectAll("dot")
        .data(data)
        .enter()
        .append("circle")
        .attr("id", d => d.id)
        .attr("cx", function (d) { return x(d[layer]['hidden'][0]); })
        .attr("cy", function (d) { return y(d[layer]['hidden'][1]); })
        .attr("r", r)
        .style("fill", "#619CFF")


    /////////////////tip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .html(d => d.sentence);

    circleG.on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    circleG.call(tip);


    //////////////////brush
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
                    x(d[layer]['hidden'][0]) >= extent[0][0] &&
                    x(d[layer]['hidden'][0]) <= extent[1][0] &&
                    y(d[layer]['hidden'][1]) >= extent[0][1] &&
                    y(d[layer]['hidden'][1]) <= extent[1][1];
                if (selected) {
                    select_data.push(d);
                }
                return selected;
            });

    }



}

function update_scatter_cls(layer) {
    //svg0.selectAll("circle").remove()
    console.log(layer)
    svg0
        .selectAll("circle")
        .transition()
        .duration(1000)
        .attr("id", d => d.id)
        .attr("cx", function (d) { return x(d[layer]['hidden'][0]); })
        .attr("cy", function (d) { return y(d[layer]['hidden'][1]); })

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
                    x(d[layer]['hidden'][0]) >= extent[0][0] &&
                    x(d[layer]['hidden'][0]) <= extent[1][0] &&
                    y(d[layer]['hidden'][1]) >= extent[0][1] &&
                    y(d[layer]['hidden'][1]) <= extent[1][1];
                if (selected) {
                    select_data.push(d);
                }
                return selected;
            });

    }




}
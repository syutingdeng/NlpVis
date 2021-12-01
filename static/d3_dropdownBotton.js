var layer = ["layer0", "layer1", "layer2", "layer3", "layer4",
    "layer5", "layer6", "layer7", "layer8", "layer9",
    "layer10", "layer11", "layer12",]
var dropdownButton = d3.select("#LayerSelection")
    .append('select')

dropdownButton // Add a button
    .selectAll('myOptions') // Next 4 lines add 6 options = 6 colors
    .data(layer)
    .enter()
    .append('option')
    .text(function (d) { return d; }) // text showed in the menu
    .attr("value", function (d) { return d; }) // corresponding value returned by the button

dropdownButton.on("change", function (d) {
    var selectedOption = d3.select(this).property("value")
    update_scatter_cls(layer = selectedOption)
})





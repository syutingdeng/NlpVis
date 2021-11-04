
$(function () {
  $('a#calculate').bind('click', function () {
    $.getJSON($SCRIPT_ROOT + '/_get_embedding',
      function (data) {
        console.log("data", data)
        draw_scatter(data,r=5)

      });
    return false;
  });
});

$(function () {
  $('a#draw').bind('click', function () {
    var data = new Array();
    $(".selected").each(function () {
      data.push($(this).attr("id"))
    })
    var data_id = {
      ids: JSON.stringify(data)

    }

    $.ajax({
      type: 'post',
      url: "/_return_select",
      data: data_id,
      success: function (d) {
        console.log("line_chart_data", d)
        drawLineChart(d.result)
        drawScoreLineChart(d.score)
        drawAttentionLineChart(d.attention)
        drawBarPlot(d.pos[10])
        drawBarPlot(d.pos[11])
        drawBarPlot(d.pos[12])

      }

    });
  });
})



$(function () {
  $('a#all_hidden').bind('click', function () {
    $.ajax({
      type: 'get',
      url: "/_all_hidden",
      success: function (d) {
        console.log("check", d)
        draw_scatter_zoom(d)
      
      },
      

    });
  });
})

$(document).ready(function () {
  $.ajax({
    type: 'get',
    url: "/_get_sentence",
    success: function (d) {
      //console.log(d.all_dataset)
      draw_scatter_cls(d.all_dataset, layer = "layer0", r = 5)
    }
  })
})



$(function () {
  $('a#calculate').bind('click', function () {
    $.getJSON($SCRIPT_ROOT + '/_get_embedding',
      function (data) {
        console.log("data", data)
        draw_scatter(data.result, r = 5)
        draw_scatter_json(data.hidden0, r = 5)
        draw_scatter_json(data.hidden4, r = 5)
        draw_scatter_json(data.hidden7, r = 5)
        draw_scatter_json(data.hidden12, r = 5)

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
        // console.log("line_chart_data", d)
        // drawLineChart(d.result)
        // drawScoreLineChart(d.score)
        // drawAttentionLineChart(d.attention)
        // drawBarPlot(d.pos[10])
        // drawBarPlot(d.pos[11])
        // drawBarPlot(d.pos[12])

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

$(function () {
  $('#seq').bind('click', function () {
    $.ajax({
      type: 'get',
      url: "/_get_sentence",
      success: function (d) {
        //console.log(d.all_dataset)
        draw_scatter(d.all_dataset, r = 5)
      }
    })
  })
})


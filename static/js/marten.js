var api_endpoint = 'api/codes';

d3.json(api_endpoint, function(dataset) {
    'use strict';

    Pace.start()

    var width = 360;
    var height = 360;
    var radius = Math.min(width, height) / 2;
    var donutWidth = 75;
    var legendRectSize = 18;
    var legendSpacing = 4;

    var color = d3.scaleOrdinal(d3.schemeCategory20b);

    var svg = d3.select('#chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width / 2) +
            ',' + (height / 2) + ')');

    var arc = d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius);

    var pie = d3.pie()
        .value(function(d) { return d.count; })
        .sort(null);

    var path = svg.selectAll('path')
        .data(pie(dataset._items))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', function(d, i) {
            return color(d.data.status_code);
        });

    var legend = svg.selectAll('.legend')
        .data(color.domain())
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
            var height = legendRectSize + legendSpacing;
            var offset =  height * color.domain().length / 2;
            var horz = -2 * legendRectSize;
            var vert = i * height - offset;
            return 'translate(' + horz + ',' + vert + ')';
        });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', color)
        .style('stroke', color);

    legend.append('text')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function(d) { return d; });

    $.fn.editable.defaults.mode = 'inline';
    $.fn.editable.defaults.params = function(params) { return JSON.stringify(params); };
    $.fn.editable.defaults.type = 'text';
    $.fn.editable.defaults.validate = function (value) {
        value = $.trim(value);
        if (!value) {
            return 'This field is required';
        }
        return '';
    };

    var $table = $('#table')
    $table.on('editable-init.bs.table', function() {
        $('.editable').on('init', function(e, edt) {
            console.log(edt)
            edt.options.url = api_endpoint + '/' + edt.options.pk;
            edt.options.ajaxOptions = {
                type: 'patch',
                dataType: 'json',
                contentType: 'application/json',
            };
        })
    });
    $table.bootstrapTable({
        columns: [{
            field: '_id',
            title: 'ID'
        }, {
            field: 'status_code',
            title: 'Status Code',
            editable: {}
        }, {
            field: 'payload',
            title: 'Payload',
            editable: {}
        }, {
            field: 'probability',
            title: 'Probability',
            editable: {}
        },{
            field: 'count',
            title: 'Count'
        }],
        data: dataset._items
    });
    Pace.stop()
});

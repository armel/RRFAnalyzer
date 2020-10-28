//
// Test float
//

function is_float(n) {
    return Number(n) === n && n % 1 !== 0;
}

//
// Format number
//

function number_format(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

//
// Format date
//

function date_format(x){
    var p = x.split("/")
    return [p[2],p[1],p[0] ].join("/")
}

//
// Total table 
//

function tabulate_total(data, columns, selector, title, legend, width) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    var table = d3.select(selector)
                .append('table')
                .attr('width', width + 'px');

    var thead = table.append('thead');
    var tbody = table.append('tbody');

    // Append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function(column) {
            return column;
        });

    // Create a row for each object in the data
    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr');

    // Create a cell in each row for each column
    var cells = rows.selectAll('td')
        .data(function(row) {
            return columns.map(function(column) {
                return {
                    column: column,
                    value: row[column]
                };
            });
        })
        .enter()
        .append('td')
        .html(function(d, i) {
            if (d.column == 'TX total' || d.column == 'Intempestifs total') {
                return number_format(d.value);
            }
            else if (d.column == 'TX moyen') {
                return d.value.toFixed(2) + 's';
            } 
            else if (d.column == 'Salon') {
                return '<a href="#' + d.value + '">' + d.value + '</a>';
            }
            else {
                return d.value;
            }
        });

    return table;
}

//
// Header table (by room)
//

function tabulate_header(data, columns, selector, title, legend, width) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    var table = d3.select(selector)
                .append('table')
                .attr('width', width + 'px');

    var thead = table.append('thead');
    var tbody = table.append('tbody');

    // Append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function(column) {
            return column;
        });

    // Create a row for each object in the data
    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr');

    // Create a cell in each row for each column
    var cells = rows.selectAll('td')
        .data(function(row) {
            return columns.map(function(column) {
                return {
                    column: column,
                    value: row[column]
                };
            });
        })
        .enter()
        .append('td')
        .html(function(d, i) {
            if (d.column == 'TX total' || d.column == 'Intempestifs total') {
                return number_format(d.value);
            }
            else if (d.column == 'TX moyen') {
                return d.value.toFixed(2)+'s';
            } 
            else {
                return d.value;
            }
        });

    return table;
}

//
// Log table (sortable)
//

function tabulate_log(data, columns, selector, title, width) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    var table = d3.select(selector)
                .append('table')
                .attr('width', width + 'px');

    var thead = table.append('thead');
    var tbody = table.append('tbody');

    var sortInfo = {
        key: 'Pos',
        order: d3.descending
    };

    // Append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .attr('class','order')
        .on('click', function(d, i) {
            create_table_body(data, d);
        })
        .text(function(column) {
            return column;
        });

    create_table_body(data, 'id');

    function create_table_body(data, sortKey) {
        if (sortInfo.order.toString() == d3.ascending.toString()) {
            sortInfo.order = d3.descending;
        } else {
            sortInfo.order = d3.ascending;
        }

        data.sort(function(x, y) {
            return sortInfo.order(x[sortKey], y[sortKey]);
        });

        data_copy = data.slice();

        var indice = 1;
        data_copy.forEach(function(d) {
            d.Pos = indice;
            indice++;
        });

        tbody
            .selectAll('tr')
            .data(data_copy)
            .enter()
            .append('tr')
            .selectAll('td')
            .data(function(d) {
                return d3.entries(d);
            })
            .enter()
            .append('td')
            .text(function(d) {
                return d.value;
            });

        tbody
            .selectAll('tr')
            .data(data_copy)
            .selectAll('td')
            .data(function(row) {
                return columns.map(function(column) {
                    return {
                        column: column,
                        value: row[column]
                    };
                });
            })
            .text(function(d) {
                if (d.column == 'TX moyen') {
                    if (is_float(d.value)) {
                        return d.value.toFixed(2) + 's';
                    } else if (d.value == -1) {
                        return '∞';
                    } else {
                        return d.value + '.00s';
                    }                
                } 
                else if (d.column == 'Emission cumulée') {
                    d.value = d.value.replace(/^0+/, '');
                    if (d.value[0] == 'h') {
                        d.value = d.value.replace(/^h +/, '');
                        d.value = d.value.replace(/^0+/, '');
                        if (d.value[0] == 'm') {
                            d.value = d.value.replace(/^m +/, '');
                            if (d.value == '00s') {
                                d.value = '-';
                            }
                        }
                    }
                    return d.value;
                } 
                else if (d.column == 'TX total' || d.column == 'Intempestifs total') {
                    return number_format(d.value);
                }
                else if (d.column == 'Last') {
                    return date_format(d.value);
                }
                else if (d.column == 'Ratio') {
                    if (is_float(d.value)) {
                        return d.value.toFixed(2);
                    } else if (d.value == -1) {
                        return '∞';
                    } else {
                        return d.value + '.00';
                    }
                } else {
                    return d.value;
                }
            });
    }
}

//
// Graph
//

function graph(data, selector, columnWidth) {
    d3.select(selector).html('');

    var margin = { top: 40, right: 40, bottom: 70, left: 60 },
        width = columnWidth - margin.left,
        height = Math.max(width / 2, 250) - margin.top - margin.bottom,
        tooltip = { width: 110, height: 30, x: -55, y: -20 };

    var parseDate = d3.time.format("%d/%m/%Y").parse,
        bisectDate = d3.bisector(function(d) { return d.date; }).left,
        formatValue = d3.format(","),
        dateFormatter = d3.time.format("%d/%m/%y");

    var x = d3.time.scale()
            .range([0, width]);

    var y = d3.scale.linear()
            .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .tickFormat(dateFormatter);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(function(d) {
            tmp = new Date(d * 1000).toISOString().substr(11, 5)+'m'
            tmp = tmp.replace(':', 'h ')
            return tmp
        });

    var area = d3.svg.area()
        .x(function(d) { return x(d.date); })
        .y0(height)
        .y1(function(d) { return y(d.secondes); })
        .interpolate("cardinal");

    var line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.secondes); })
        .interpolate("cardinal");

    var svg = d3.select(selector).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data.forEach(function(d) {
        d.date = parseDate(d.Date);
        d.secondes = d.Secondes;
    });

    data.sort(function(a, b) {
        return a.date - b.date;
    });

    x.domain([data[0].date, data[data.length - 1].date]);
    y.domain(d3.extent(data, function(d) { return d.secondes; }));

    svg.append("g")
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + (height + 0.5) + ')')
        .call(xAxis)
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '-.55em')
        .attr('transform', 'rotate(-45)');

    svg.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(0,0)")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(0)")
        .attr("x", 100)
        .attr("y", 0)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Emission cumulée");

    svg.append("path")
       .data([data])
       .attr("class", "area")
       .attr("d", area);

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    var focus = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("circle")
        .attr("r", 5);

    focus.append("rect")
        .attr("class", "tooltip")
        .attr("width", 110)
        .attr("height", 30)
        .attr("x", -55)
        .attr("y", -40)
        .attr("rx", 4)
        .attr("ry", 4);

    focus.append("text")
        .attr("class", "tooltip-date")
        .attr("x", -51)
        .attr("y", -20);

    focus.append("text")
        .attr("class", "tooltip-likes")
        .attr("x", 4)
        .attr("y", -20);

    svg.append("rect")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
        var x0 = x.invert(d3.mouse(this)[0]),
            i = bisectDate(data, x0, 1),
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        focus.attr("transform", "translate(" + x(d.date) + "," + y(d.secondes) + ")");
        focus.select(".tooltip-date").text(dateFormatter(d.date));
        focus.select(".tooltip-likes").text(
            tmp = new Date(d.secondes * 1000).toISOString().substr(11, 5).replace(':', 'h ')+'m'
        );
    }
}

//
// Stat table
//

function tabulate_stat(data, columns, selector, title, legend, width) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    var table = d3.select(selector)
                .append('table')
                .attr('width', width + 'px');

    var thead = table.append('thead');
    var tbody = table.append('tbody');

    var url = location.protocol + '//' + location.host + location.pathname;
    var value = ['d', 'w', 'm', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'd60', 'd120', 'd180', 'd240', 'd300', 'd360'];
    var indice = 0;

    // Append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns)
        .enter()
        .append('th')
        .text(function(column) {
            return column;
        });

    // Create a row for each object in the data
    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr');

    // Create a cell in each row for each column
    var cells = rows.selectAll('td')
        .data(function(row) {
            return columns.map(function(column) {
                return {
                    column: column,
                    value: row[column]
                };
            });
        })
        .enter()
        .append('td')
        .html(function(d, i) {
            arg = value[indice];
            indice += 1;
            return '<a href="' + url + '?stat=' + arg + '">' + d.value + '</a>'; 
        });

    return table;
}

//
// Cumulative emission
//

function emission(selector, time, title, width) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    d3.select(selector)
        .append('div')
        .attr('class', 'container')
        .append('div')
        .attr('class', 'center-clock')
        .append('div')
        .attr('class', 'clock');

    d3.select(selector)
        .append('table')
        .attr('width', width + 'px')
        .attr('class', 'transmit');

        clock = $('.clock').FlipClock(time, {
            clockFace: 'HourlyCounter',
            countdown: true,
            showSeconds: false
        });

    clock.stop(function() {});
}

//
// Change color
//

function color(colorSelected) {

    var newColor;

    if (colorSelected == 'SteelBlue') {
        newColor = 'ForestGreen';
    }
    else if (colorSelected == 'ForestGreen') {
        newColor = 'DarkOrange';
    }
    else if (colorSelected == 'DarkOrange') {
        newColor = 'DarkCyan';
    }
    else if (colorSelected == 'DarkCyan') {
        newColor = 'DarkMagenta';
    }
    else if (colorSelected == 'DarkMagenta') {
        newColor = 'DarkKhaki';
    }
    else if (colorSelected == 'DarkKhaki') {
        newColor = 'DimGray';
    }
    else if (colorSelected == 'DimGray') {
        newColor = 'Crimson';
    }
    else if (colorSelected == 'Crimson') {
        newColor = 'SteelBlue';
    }

    localStorage.setItem('color', newColor);

    window.location.reload(false); 
    return 0;
}

//
// Highlight search
//

$(function() {

  var mark = function() {

    // Read the keyword
    var keyword = $("input[name='keyword']").val();

    // Determine selected options
    var options = {"accuracy": "partialy"};
    $("input[name='opt[]']").each(function() {
      options[$(this).val()] = $(this).is(":checked");
    });

    // Remove previous marked elements and mark
    // the new keyword inside the context
    $(".columns").unmark({
      done: function() {
        $(".columns").mark(keyword, options);
      }
    });
  };

  $("input[name='keyword']").on("input", mark);
  $("input[type='checkbox']").on("change", mark);

});
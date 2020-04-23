function is_float(n) {
    return Number(n) === n && n % 1 !== 0;
}

function number_format(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

function tabulate(data, columns, selector, title, legend, width) {
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
            else {
                return d.value;
            }
        });

    return table;
}

function tabulate_order(data, columns, selector, title, width) {
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
            return sortInfo.order(x[sortKey], y[sortKey])
        });

        data_copy = data.slice();

        var indice = 1
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
                return d3.entries(d)
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
                if (d.column == 'TX total' || d.column == 'Intempestifs total') {
                    return number_format(d.value);
                }
                if (d.column == 'Ratio') {
                    if (is_float(d.value)) {
                        return d.value.toFixed(2)
                    } else if (d.value == -1) {
                        return '∞';
                    } else {
                        return d.value + '.00'
                    }
                } else {
                    return d.value;
                }
            });
    }
}

function emission(selector, time) {
    d3.select(selector)
        .append('div')
        .attr('class', 'container')
        .append('div')
        .attr('class', 'center-clock')
        .append('div')
        .attr('class', 'clock')

        clock = $('.clock').FlipClock(time, {
            clockFace: 'HourlyCounter',
            countdown: true,
            showSeconds: false
        });
        
    clock.stop(function() {});
}

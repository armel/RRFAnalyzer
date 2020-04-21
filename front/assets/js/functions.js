function is_float(n) {
    return Number(n) === n && n % 1 !== 0;
}

function tabulate(data, columns, selector, title) {
    d3.select(selector).html('');
    d3.select(selector).append('h2').html(title);

    var table = d3.select(selector).append('table');
    var thead = table.append('thead');
    var tbody = table.append('tbody');

    // Append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns).enter()
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
            return d.value;
        });

    return table;
}
;
(function() {

    d3.json('analyzer.json', function(error, data) {
        if (error) {
            return console.warn('Erreur', error);
        } else {

            abstract = data['abstract']
            log = data['log']

            const containerSelector = '.abstract-table';
            const containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> Résumé';

            tabulate(abstract, ['Links', 'Durée', 'TX', 'Intempestif'], containerSelector, containerTitle); // 4 columns table

            var sortInfo = {
                key: 'Pos',
                order: d3.descending
            };

            /*
            var table = d3.select('body').insert('table', ':first-child').attr('id', 'NameList');
            var thead = table.append('thead');
            var tbody = table.append('tbody');
            */

            d3.select('.log-table').html('');
            d3.select('.log-table').append('h2').html("Log");

            var table = d3.select('.log-table').append('table');
            var thead = table.append('thead');
            var tbody = table.append('tbody');

            thead.append('tr')
                .selectAll('th')
                .data(d3.entries(log[0]))
                .enter()
                .append('th')
                .on('click', function(d, i) {
                    create_table_body(d.key);
                })
                .text(function(d) {
                    return d.key;
                });

            create_table_body('id');

            function create_table_body(sortKey) {
                if (sortInfo.order.toString() == d3.ascending.toString()) {
                    sortInfo.order = d3.descending;
                } else {
                    sortInfo.order = d3.ascending;
                }

                log.sort(function(x, y) {
                    return sortInfo.order(x[sortKey], y[sortKey])
                });

                log_copy = log.slice();

                var indice = 1
                log_copy.forEach(function(d) {
                    d.Pos = indice;
                    indice++;
                });

                tbody
                    .selectAll('tr')
                    .data(log_copy)
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
                    .data(log_copy)
                    .selectAll('td')
                    .data(function(d) {
                        return d3.entries(d)
                    })
                    .text(function(d) {
                        if (d.key == 'Ratio') {
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
    });
})();
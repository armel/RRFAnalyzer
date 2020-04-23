;
(function() {
    // Initialise color
    if (localStorage.getItem('color') === null) {
        localStorage.setItem('color', 'DarkOrange');
    }
    
    var colorSelected = localStorage.getItem('color');

    var bodyStyles = document.body.style;
    bodyStyles.setProperty('--color-theme', colorSelected);

    // Set the dimensions of the canvas

    const columnWidth = document.querySelector('.columns :first-child').clientWidth;

    const margin = {
                top: 20,
                right: 20,
                bottom: 70,
                left: 40
            },
            width = columnWidth - margin.left - margin.right,
            height = Math.max(width / 3, 250) - margin.top - margin.bottom;


    d3.json('analyzer.json', function(error, data) {
        if (error) {
            return console.warn('Erreur', error);
        } else {
            var room = ['ALL', 'RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL'];
            var containerSelector;
            var containerTitle;
            var containerLegend;

            room.forEach(function(r) {
                if (r == 'ALL') {
                    var where = 'général' 
                }
                else {
                    var where = 'du salon ' + r
                }

                containerSelector = '.abstract-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> Résumé ' + where;
                containerLegend = 'Ce tableau présente le résumé de l\'activité ' + where + ' : émission cumulée, nombre total de links actifs, de passages en émission et de déclenchements intempestifs. ';

                tabulate(data[r]['abstract'], ['Emission cumulée', 'Links total', 'TX total', 'Intempestifs total'], containerSelector, containerTitle, containerLegend, width + margin.left + margin.right); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);

                containerSelector = '.log-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> Log ' + where;
                containerLegend = 'Ce tableau présente l\'activité ' + where + ' par link : émission cumulée, nombre total de passages en émission, de déclenchements intempestifs et ratio. Le ratio est calculé en divisant le nombre de secondes en émission par le nombre de déclenchements intempestifs. Plus ce ratio est faible, plus le link est perturbant...';

                tabulate_order(data[r]['log'], ['Pos', 'Indicatif', 'Emission cumulée', 'TX total', 'Intempestifs total', 'Ratio'], containerSelector, containerTitle, width + margin.left + margin.right); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            });

            containerSelector = '.tot-graph'
            containerTitle = '<div class="icon"><i class="icofont-mic"></i></div> Emission cumulée'
            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').html(containerTitle);

            console.log(data['Counter'])
            emission(containerSelector, data['Counter'])
        }
    });
})();
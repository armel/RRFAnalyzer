;
(function() {
    // Get JSON Flux

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var stat = urlParams.get('stat')
    var when = ''

    if(stat === null) {
        stat = 'm'
    }

    // Initialise color
    if (localStorage.getItem('color') === null) {
        localStorage.setItem('color', 'DarkOrange');
    }
    
    var colorSelected = localStorage.getItem('color');

    var bodyStyles = document.body.style;
    bodyStyles.setProperty('--color-theme', colorSelected);

    // No cach

    const noCache = new Date().getTime();

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


    d3.json('analyzer_' + stat + '.json', function(error, data) {
        if (error) {
            return console.warn('Erreur', error);
        } else {
            var room = ['Global', 'RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL'];
            var elsewhere = [];
            var containerSelector;
            var containerTitle;
            var containerLegend;

            room.forEach(function(r) {
                if (r == 'Global') {
                    var where = 'globale' 
                }
                else {
                    var where = 'du salon ' + r
                }
                elsewhere.push(data[r]['abstract'][0])

                containerSelector = '.abstract-' + r.toLowerCase();
                containerTitle = '<div id=' + r + ' class="icon"><i class="icofont-info-circle"></i></div> Synthèse ' + where;
                containerLegend = 'Ce tableau présente la synthèse de l\'activité ' + where + ' : émission cumulée, nombre total de links actifs, de passages en émission (et durée moyenne) et de déclenchements intempestifs. ';

                tabulate(data[r]['abstract'], ['Emission cumulée', 'Links total', 'TX total', 'TX moyen', 'Intempestifs total'], containerSelector, containerTitle, containerLegend, width + margin.left + margin.right); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);

                if (where == 'globale') {
                    where_patch = 'global'
                }
                else {
                    where_patch = where                    
                }

                containerSelector = '.log-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> Log ' + where_patch;
                containerLegend = 'Ce tableau présente l\'activité ' + where + ' par link : émission cumulée, nombre total de passages en émission, de déclenchements intempestifs et ratio. Le ratio est calculé en divisant le nombre de secondes en émission par le nombre de déclenchements intempestifs. Plus ce ratio est faible, plus le link est perturbant...';

                tabulate_order(data[r]['log'], ['Pos', 'Indicatif', 'Emission cumulée', 'TX total', 'TX moyen', 'Intempestifs total', 'Ratio'], containerSelector, containerTitle, width + margin.left + margin.right); // 4 columns table
                d3.select(containerSelector).append('span').text(containerLegend);
            });

            containerSelector = '.abstract-elsewhere';
            containerTitle = '<div class="icon"><i class="icofont-dashboard-web"></i></div> Synthèse globale et par salon ' + data['When'] + ' (<a href="http://rrf.f5nlg.ovh:8080/RRFTracker/RRF-today/">accès au RRFTracker</a>)'
            containerLegend = 'Ce tableau présente la synthèse totale et par salon de l\'activité : émission cumulée, nombre total de links actifs, de passages en émission (et durée moyenne) et de déclenchements intempestifs. ';

            tabulate_elsewhere(elsewhere, ['Salon', 'Emission cumulée', 'Links total', 'TX total', 'TX moyen', 'Intempestifs total'], containerSelector, containerTitle, containerLegend, width + margin.left + margin.right); // 4 columns table
            d3.select(containerSelector).append('span').text(containerLegend);

            containerSelector = '.tot-graph'
            containerTitle = '<div class="icon"><i class="icofont-wall-clock"></i></div> Emission cumulée'
            containerLegend = 'Ce compteur affiche la durée émission cumulée en heures et minutes.';

            emission(containerSelector, data['Counter'], containerTitle, width + margin.left + margin.right);
            d3.select(containerSelector).append('span').text(containerLegend);

            containerSelector = '.search-graph'
            containerTitle = '<div class="icon"><i class="icofont-search-stock"></i></div> Moteur de recherche'

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('h2').html(containerTitle);

            containerSelector = '.stat-table'
            containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> Autres statistiques'
            containerLegend = 'Ce tableau permet de pointer vers d\'autres stats.';

            tabulate_stat(data['Stat'], ['Autres stats'], containerSelector, containerTitle, containerLegend, width + margin.left + margin.right); // 4 columns table
            d3.select(containerSelector).append('span').text(containerLegend);

            containerSelector = '.author-legend';
            var containerAuthor = '<a href="https://github.com/armel/RRFAnalyzer">RRFAnalyzer</a> est un projet Open Source, développé par <a href="https://www.qrz.com/db/F4HWN">F4HWN Armel</a>, sous licence MIT.<br>Couleur actuelle du thème <a onClick="color(\'' + colorSelected + '\');">' + colorSelected + '</a>.';

            d3.select(containerSelector).html('');
            d3.select(containerSelector).append('span')
                .attr('class', 'author')
                .html(containerAuthor);

        }
    });
})();
;
(function() {
    d3.json('analyzer.json', function(error, data) {
        if (error) {
            return console.warn('Erreur', error);
        } else {
            var room = ['RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL'];
            var containerSelector;
            var containerTitle;


            room.forEach(function(r) {

                abstract = data[r]['abstract']
                //log = data[r]['log']

                containerSelector = '.abstract-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> Résumé du salon ' + r;

                console.log(containerSelector);

                tabulate(abstract, ['Emission cumulée', 'Links total', 'TX total', 'Intempestifs total'], containerSelector, containerTitle); // 4 columns table

                containerSelector = '.log-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> Log du salon ' + r;

                tabulate_order(data[r]['log'], ['Pos', 'Indicatif', 'Emission cumulée', 'TX total', 'Intempestifs total', 'Ratio'], containerSelector, containerTitle); // 4 columns table
            });
        }
    });
})();
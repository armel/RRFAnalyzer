;
(function() {
    d3.json('analyzer.json', function(error, data) {
        if (error) {
            return console.warn('Erreur', error);
        } else {
            var room = ['RRF', 'TECHNIQUE', 'INTERNATIONAL', 'BAVARDAGE', 'LOCAL'];
            var containerSelector;
            var containerTitle;

            containerSelector = '.abstract-all';
            containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> Résumé total';

            tabulate(data['ALL']['abstract'], ['Emission cumulée', 'Links total', 'TX total', 'Intempestifs total'], containerSelector, containerTitle); // 4 columns table

            room.forEach(function(r) {
                containerSelector = '.abstract-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-info-circle"></i></div> Résumé du salon ' + r;

                tabulate(data[r]['abstract'], ['Emission cumulée', 'Links total', 'TX total', 'Intempestifs total'], containerSelector, containerTitle); // 4 columns table

                containerSelector = '.log-' + r.toLowerCase();
                containerTitle = '<div class="icon"><i class="icofont-spreadsheet"></i></div> Log du salon ' + r;

                tabulate_order(data[r]['log'], ['Pos', 'Indicatif', 'Emission cumulée', 'TX total', 'Intempestifs total', 'Ratio'], containerSelector, containerTitle); // 4 columns table
            });
        }
    });
})();
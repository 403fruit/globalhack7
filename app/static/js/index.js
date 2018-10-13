(function () {
    var bloodhound_resources = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: '/api/en/resources',
            filter: false
        }
    });

    localStorage.clear();
    bloodhound_resources.initialize();

    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'resources',
        source: bloodhound_resources.ttAdapter()
    });
})();
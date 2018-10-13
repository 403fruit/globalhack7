(function () {
    var url = '/api/resources?lang_code=' + window.lang_code;

    var bloodhound_resources = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: {
            url: url,
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
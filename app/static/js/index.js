(function () {
    var url = '/api/resources?query=%QUERY&lang_code=' + window.lang_code;

    var bloodhound_resources = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: url,
            wildcard: '%QUERY'
        }
    });

    bloodhound_resources.initialize();

    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'resources',
        source: function (query, callback) {
            var comp = (
                (query.charCodeAt(0) - 0xD800) * 0x400
              + (query.charCodeAt(1) - 0xDC00) + 0x10000
            );
            comp = comp.toString("16");
            if (comp < 0) {
                bloodhound_resources.get(comp)
            } else {
                bloodhound_resources.get(query)
            }
        }
    });
})();
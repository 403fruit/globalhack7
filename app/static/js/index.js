(function () {
    var url = '/api/resources_autosuggest?query=%QUERY&lang_code=' + window.lang_code;

    var bloodhound_resources = new Bloodhound({
        datumTokenizer: function (datum) {
            return Bloodhound.tokenizers.whitespace(datum);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: url,
            wildcard: '%QUERY',
            filter: function(data) {
                return $.map(data, function(resources, label) {
                    return {
                        value: resources,
                        label: label,
                    }
                }.bind(this));
            }.bind(this)
        },
    });

    bloodhound_resources.initialize();

    $('.typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        displayKey: 'label',
        templates: {
            suggestion: function(suggestion) {
                return '<p>' + suggestion.label + '</p>';
            }
        },
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

    $('#resource').on('typeahead:selected', function(event, value) {
        var resources = value.resources;
    });
})();

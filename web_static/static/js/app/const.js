/* JSHint strict mode tweak */
/*global $:false */
/*global Firebat:false */
/*global Ember:false */
/*global Mousetrap:false */
/*global console:false */

/* constant variables */
var CONST = (function() {
	'use strict';
    var priv = {
        'API_BASE_PATH': '/api/v1/',
        'TEST_PER_PAGE': 2,
        'TEST_STATUS': {
            '1': 'created',
            '2': 'started',
            '3': 'running',
            '4': 'aborted',
            '5': 'finished'
        },
        'DELIM_LINKS': ",",
        'DELIM_LINK_PARAM':  ";"
     };

     return {
        get: function(name) { return priv[name]; }
    };
})();

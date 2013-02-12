/* JSHint strict mode tweak */
/*global $:false */
/*global ya:false */
/*global helpers:false */
/*global CONST:false */
/*global Firebat:false */
/*global Ember:false */
/*global Mousetrap:false */
/*global console:false */

/* app */
(function( win ) {
	'use strict';

	win.Firebat = Ember.Application.create({
        LOG_TRANSITIONS:true,
        Store: DS.Store.extend({
            revision: 11
        }),
		ApplicationController: Ember.Controller.extend({
            needs: ['settings', 'tests'],
            prefetch: function() {
                var self = this;
                self.get('controllers.settings').fetch();
                self.get('controllers.tests').goToPage();
            },
            logoutLink: ya.getLogoutLink()
        }),
		ready: function() {
			this.initialize();
		}
	});

})( window );


/* view */
(function( app ) {
	'use strict';

    var ApplicationView = Ember.View.extend({
        templateName:  'application',
        didInsertElement: function() {
            var self = this;
            self.get('controller').prefetch();
        }
    });

    var SettingsView = Ember.View.extend({
        templateName:  'settingsTemplate'
    });
    var TestsView = Ember.View.extend({
        templateName:  'testsTemplate',
        didInsertElement: function() {
            var self = this;
            console.info(self.get('controller'));
            //if (!(app.TestsPaginator.header)) {
            //    console.info('Emptie');
            //    self.get('controller').goToPage();
            //}
            //console.info(app.TestsPaginator.header);
            self.get('controller').goToPage();
            Mousetrap.bind('ctrl+right', function() {
                self.get('controller').goToPage('next');
            });
            Mousetrap.bind('ctrl+left', function() {
                self.get('controller').goToPage('prev');
            });
        },
        wilLRemoveElement: function() {
            Mousetrap.unbind('ctrl+right');
            Mousetrap.unbind('ctrl+left');
        }
    });
    var TestView = Ember.View.extend({
        templateName:  'testTemplate'
    });
    var TanksView = Ember.View.extend({
        templateName:  'tanksTemplate'
    });

    app.ApplicationView = ApplicationView;
    app.SettingsView = SettingsView;
    app.TestsView = TestsView;
    app.TestView = TestView;
    app.TanksView = TanksView;

})( window.Firebat);

/* model */
(function( app ) {
    'use strict';

    app.Settings = Ember.Object.create({
        /* User UI and notification settings */
        fetched_at: null,
        fetched_hum: null,
        avatarURL: null,
        data: null,
        update: function(data) {
            //console.info('Settings model update fired');
            this.fetched_at = helpers.epoach();
            this.set('fetched_hum', Date());
            this.set("data", data);
            this.set("avatarURL", ya.getAvatarLink(data.login));
        }.observes("settings")
    });

    app.Test = Ember.Object.extend({
        /* Load test entrie */
        started_at: null,
        ended_at: null,
        status_id: null,
        owner: null,
        id: null,
        test_name: null
    });

    app.TestsPaginator = Ember.Object.create({
        /* Paginator state */
        pages: [],
        header: null,
        perPage: null,
        newerDisabled: false,
        olderDisabled: false,
        update: function(data) {
            this.set("header", data);
            if (!("prev" in data)) {
                this.set("newerDisabled", true);
            } else {
                this.set("newerDisabled", false);
            }
            if (!("next" in data)) {
                this.set("olderDisabled", true);
            } else {
                this.set("olderDisabled", false);
            }

        },
        reset: function() {
            this.set("header", null);
            this.set("currPage", null);
            this.set("newerDisabled", false);
            this.set("olderDisabled", false);
        }
    });


})( window.Firebat);

/* controller */
(function( app ) {
    'use strict';

    var SettingsController = Ember.Controller.extend({
        fetch: function() {
          var self = this;
          $.ajax({
            url: [CONST.get('API_BASE_PATH'), 'user/settings'].join(''),
            dataType: 'json',
            statusCode: {
                401: function (response) {
                    console.info('Auth failed.');
                    ya.redirectToAuth();
                }
            },
            success: function(data) {
                app.Settings.update(data);
            },

            error: function() {
              console.info('Can\'t fetch *settings* from API');
            }
          });
        }
    });

    var TestsController = Ember.ArrayController.extend({
        needs: [''],
        newerDisabled: function() {
            return app.TestsPaginator.newerDisabled;
        }.property('content.newerDisabled'),
        olderDisabled: function() {
            return app.TestsPaginator.olderDisabled;
        }.property('content.olderDisabled'),
        nextStr: 'next',
        prevStr: 'prev',
        echo: function() {
            console.log('EHLO...');
        },
        reload: function() {
            //console.info('Reloading *tests* data from server side.');
            app.TestsPaginator.reset();
            this.goToPage();
        },
        createTestFromJSON: function(json) {
            var t = app.Test.create(json);
            t.status_name = CONST.get('TEST_STATUS')[t.status_id];
            if (t.started_at) {
                t.started_at = new Date(t.started_at);
            }
            if (t.ended_at) {
                t.ended_at = new Date(t.ended_at);
            }
            t.started_at_pp = helpers.dateToStr(t.started_at); 
            t.ended_at_pp = helpers.dateToStr(t.ended_at); 
            //console.info(typeof t.id);
            return t;
        },
        fetch: function(url, params) {
          var self = this;
          var defaultParams = {
            'owner': 'gkomissarov',
            'per_page': CONST.get('TEST_PER_PAGE')
          };
          if (typeof url == 'undefined') {
            if (typeof params == 'undefined') {
                params = defaultParams;
            }
            url = [CONST.get('API_BASE_PATH'), 'test?', $.param(params)].join('');
          }

          $.ajax({
            url: url,
            dataType: 'json',
            statusCode: {
                401: function (response) {
                    console.info('Auth failed.');
                    ya.redirectToAuth();
                }
            },
            success: function(data, textStatus, XMLHttpRequest) {
                var linkHeader = XMLHttpRequest.getResponseHeader('Link');
                var header = helpers.parseLinkHeader(linkHeader);
                app.TestsPaginator.update(header);
                var tests = data.tests;
                tests = tests.map(function(item) {
                    return self.createTestFromJSON(item);
                });
                self.set('content', tests);
            },

            error: function() {
              console.info('Can\'t fetch *settings* from API');
            }
          });
        },
        goToPage: function(v) {
            var self = this;
            var url ='';
            var defaultParams = {
                'owner': 'gkomissarov',
                'per_page': app.TestsPaginator.perPage || CONST.get('TEST_PER_PAGE')
            };

            if (typeof v == 'undefined') {
                url = [CONST.get('API_BASE_PATH'), 'test?', $.param(defaultParams)].join('');
            } else {
                var direction = '';
                if (typeof v == 'string' || v instanceof String) {
                    direction = v;
                } else {
                    // old Emberjs version workaround
                    direction = v.srcElement.name;
                }
                url = app.TestsPaginator.header[direction].url;
            }
            this.fetch(url);
        }
    });

    app.SettingsController = SettingsController;
    app.TestsController = TestsController;

})( window.Firebat );


/* router */
(function( app ) {
	'use strict';

    app.Router.map(function() {
        this.route("tanks");
        this.route("settings");
        this.route("tests");
        this.resource('test', { path: '/test/:test_id' }, function() {
        });
    });

    app.TestRoute = Ember.Route.extend({
        model: function(params) {
            var testsController = this.controllerFor('tests');
            var testController = this.controllerFor('test');
            var existingModel  = testsController.findProperty('id', parseInt(params.test_id, 10));

            console.info(existingModel);
            if (existingModel) {
                return existingModel;
            }
            return testController.fetch(params.test_id);
        }
    });

    app.IndexRoute = Ember.Route.extend({
        redirect: function() {
            this.transitionTo('tests');
        }
    });
    
})( window.Firebat );

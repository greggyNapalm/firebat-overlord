/* JSHint strict mode tweak */
/*global $:false */
/*global Firebat:false */
/*global Ember:false */
/*global Mousetrap:false */
/*global console:false */

/* app */
(function( win ) {
	'use strict';

	win.Firebat = Ember.Application.create({
		VERSION: '1.0',
		rootElement: '#firebat_app',
		storeNamespace: 'firebat-emberjs',
		ApplicationController: Ember.Controller.extend({
            logoutLink: ya.getLogoutLink()
        }),
		ready: function() {
            console.log("App loaded.");
			this.initialize();
            this.router.settingsController.fetch();
            this.router.testsController.goToPage();
            Mousetrap.bind('ctrl+right', function() {
                Firebat.router.testsController.goToPage('next');
            });
            Mousetrap.bind('ctrl+left', function() {
                Firebat.router.testsController.goToPage('prev');
            });
		}
	});

})( window );


/* view */
(function( app ) {
	'use strict';

    var ApplicationView = Ember.ContainerView.extend({
        childViews: [ 'headerView', 'mainView', 'footerView' ],
        //headerView: Ember.ContainerView.create({
        headerView: Ember.View.create({
            elementId: 'header',
            classNames: ['app-header'],
            templateName: 'headerTemplate'
        }),
        //mainView: Em.ContainerView.create({
        mainView: Ember.View.create({
            elementId: 'main',
            classNames: ['app-main'],
            templateName: 'mainTemplate'
        }),
        //footerView: Ember.ContainerView.create({
        footerView: Ember.View.create({
            elementId: 'fotter',
            classNames: ['app-fotter'],
            templateName: 'fotterTemplate'
        })
	});

    //var UserView = Ember.View.extend({
    //    templateName:  'userTemplate'
    //});

    var SettingsView = Ember.View.extend({
        templateName:  'settingsTemplate'
    });
    var TestsView = Ember.View.extend({
        templateName:  'testsTemplate'
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
            console.info('Settings model update fired');
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
        //currPage: null,
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
        reload: function() {
            console.info('Reloading *tests* data from server side.');
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
                direction = v.srcElement.name;
            }
            url = app.TestsPaginator.header[direction].url;
          }
          console.info("goto: ", url);
          this.fetch(url);
        }
    });

    app.SettingsController = SettingsController;
    app.TestsController = TestsController;

})( window.Firebat );


/* router */
(function( app ) {
	'use strict';

	var Router = Ember.Router.extend({
		root: Ember.Route.extend({
			showTests: Ember.Route.transitionTo( 'tests' ),
			showTanks: Ember.Route.transitionTo( 'tanks' ),
			showSettings: Ember.Route.transitionTo( 'settings' ),

			index: Ember.Route.extend({
                route:  '/',
                redirectsTo: 'tests'
            }),
            tests: Ember.Route.extend({
                route:  '/tests',
                enter: function ( router ){
                    console.info('context -> tests');
                },
                connectOutlets:  function(router, context){
                    router.get('applicationController').connectOutlet('main', 'Tests');
                }
            }),
            test: Ember.Route.extend({
                route:  '/test/:test_id',
                connectOutlets:  function(router, context){
                    router.get('applicationController').connectOutlet('main', 'Test');
                }
            }),
            settings: Ember.Route.extend({
                route:  '/settings',
                enter: function ( router ){
                    console.log("Entrering in *settings* state.");
                },
                connectOutlets:  function(router, context){
                    router.get('applicationController').connectOutlet('main', 'Settings');
                }
            }),
            tanks: Ember.Route.extend({
                route:  '/tanks',
                connectOutlets:  function(router, context){
                    router.get('applicationController').connectOutlet('main', 'Tanks');
                }
            })
        })
    });

	app.Router = Router;

})( window.Firebat );

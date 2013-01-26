/*global module:false*/
module.exports = function(grunt) {
    grunt.loadNpmTasks('grunt-contrib');
    grunt.loadNpmTasks('grunt-ember-handlebars');
    //grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-templater');

    var js_3rd_party = [
        'static/js/3d_party/jquery-1.8.3.min.js',
        'static/js/3d_party/bootstrap.min.js',
        'static/js/3d_party/bootstrap-dropdown.js',
        'static/js/3d_party/bootstrap-tooltip.js',
        'static/js/3d_party/mousetrap.min.js',
        'static/js/3d_party/handlebars-1.0.rc.1.js',
        'static/js/3d_party/ember-1.0.0-pre.2.min.js'
    ];
    var js_firebat = [
        'static/js/app/const.js',
        'static/js/app/helpers.js',
        'static/js/app/ya.js',  //missing in GitHub version
        'static/js/app/app.js'
    ];

    var js_all = js_3rd_party.slice(0);
    js_all.push.apply(js_all, js_firebat);

    var build_num = process.env.FIRE_BUILD_NUM || new Date().getTime();
    var build_path = ['build', build_num, 'app.min.js'].join('/');

  // Project configuration.
  grunt.initConfig({
    build_num: build_num,
    build_path: build_path,
    js_all: js_all,
    meta: {
      version: '0.0.1',
      banner: '/*! Firebat Overlord - v<%= meta.version %> - ' +
        '<%= grunt.template.today("UTC:h:MM:ss TT Z") %>\n' +
        '* https://github.com/greggyNapalm/firebat-overlord\n' +
        '* Copyright (c) <%= grunt.template.today("yyyy") %> ' +
        'Gregory Komissarov; Licensed BSD */'
    },
    ember_handlebars: {
        all: {
          src: 'static/tmpl/*.hbs',
          dest: '_tmp/templates'
        }
    },
    concat: {
      dist: {
        src : ['<config:js_all>', '_tmp/templates/*.js'],
        dest: '_tmp/app.concat.js'
      }
    },
    min: {
      dist: {
        src: ['<banner:meta.banner>', '<config:concat.dist.dest>'],
        dest: '<config:build_path>'
      }
    },
    template: {
        prod: {
          src: 'static/tmpl/index.hb',
          dest: 'index.html',
          variables: {
            app_js_path: '<config:build_path>'
          }
        }
    },
    clean: ["_tmp"]
  });

  // Default task.
  grunt.registerTask('default', 'ember_handlebars concat min template:prod clean');

};

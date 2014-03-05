module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    watch: {
      options: {
        nospawn:true,
        livereload:true,
      },
      html: {
        files: ['static/index.html']
      },
      specs: {
        files: ['spec/*'],
        tasks: [
          'jasmine'
        ]
      },
      css: {
        files: [
          'static/sass/*',
        ],

        tasks: ['sass']
      },

      scripts: {
        files: ['static/scripts/*.js'],
        tasks: [
          'uglify',
          'jshint',
          'jasmine'
        ]
      }
    },

    jshint: {
      files: ['static/scripts/*.js'],
    },

    sass: {
        dist: {
          options: {
            cacheLocation: '/tmp/sass-cache',
            sourcemap: true,
            trace: true,
          },
            files: {
                'static/css/styles.css': 'static/sass/styles.scss'
            }
        }
    },

    uglify: {
      footer: {
        options: {
          sourceMappingURL: '/js/source-map.js',
          sourceMap: 'static/js/source-map.js',
          sourceMapRoot: '/',
          preserveComments: false,
          mangle: false
        },

        src: [
          'static/scripts/base.js',
        ],

        dest: 'static/js/base.js'
      }
    },

    jasmine: {
      unit: {
        src: 'static/js/*.js',
        options: {
          specs: 'spec/*Spec.js',
          helpers: 'spec/*Helper.js',
          vendor: [
          "bower_components/jquery/jquery.min.js",
          "bower_components/howler/howler.min.js",
          "bower_components/gmap3/gmap3.js"
          ]
        }
      }
    }

  });

  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jasmine');
};

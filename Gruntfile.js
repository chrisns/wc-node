// Generated on 2014-03-18 using generator-angular 0.7.1
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {

  // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);
  grunt.loadNpmTasks('grunt-exec');
  grunt.loadNpmTasks('grunt-jsonlint');
  grunt.loadNpmTasks('grunt-json-schema');
  grunt.loadNpmTasks('grunt-nose');
  grunt.loadNpmTasks('grunt-notify');
  // Configurable paths for the application
  var appConfig = {
    app: require('./bower.json').appPath || 'app',
    dist: 'dist'
  };
  // Define the configuration for all the tasks
  grunt.initConfig({

    // Project settings
    yeoman: appConfig,

    // Watches files for changes and runs tasks based on the changed files
    watch: {
      options: {
        spawn: false
      },
      bower: {
        files: ['bower.json'],
        tasks: ['wiredep']
      },
      js: {
        files: ['<%= yeoman.app %>/scripts/{,*/}*.js'],
        tasks: ['newer:jshint:all'],
        options: {
          livereload: '<%= connect.options.livereload %>'
        }
      },
      jsTest: {
        files: ['test/spec/{,*/}*.js'],
        tasks: ['newer:jshint:test', 'karma']
      },
      compass: {
        files: ['<%= yeoman.app %>/styles/{,*/}*.{scss,sass}'],
        tasks: ['compass:server', 'autoprefixer']
      },
      gruntfile: {
        files: ['Gruntfile.js']
      },
      livereload: {
        options: {
          livereload: '<%= connect.options.livereload %>'
        },
        files: [
          '<%= yeoman.app %>/{,*/}*.html',
          '.tmp/styles/{,*/}*.css',
          '<%= yeoman.app %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}'
        ]
      },
      python: {
        files: ['*.py', 'models/*.py', 'tests/**/*.py', 'WorkflowSpecs/**/*.py', 'py_utils/**/*.py'],
        tasks: ['nose']
      },
      wf: {
        files: ['WorkflowSpecs/*.bpmn', 'WorkflowSpecs/*.py'],
        tasks: ['exec:regenWorkflow', 'jsonlint:workflow']
      },
      pyrequirements: {
        files: ['requirements.txt'],
        tasks: ['clean:python', 'exec:pythonDependencies', 'nose']
      },
      schema: {
        files:['schema.json'],
        tasks:['jsonlint:schema', 'json_schema', 'nose']
      }
    },
    nose: {
      options: {
        // Task-specific options go here.
        with_coverage: true,
        virtualenv: 'env',
        cover_min_percentage: 90,
        verbose: true,
        with_gae: true,
        cover_tests: true,
        cover_xml_file: '.coverage',
        without_sandbox: true,
        with_doctest: true,
        with_xunit: true
      },
      main: {
        // Target-specific file lists and/or options go here.
      },
    },
    exec: {
      pythonDependencies: {
        cmd: 'bash -c "virtualenv env && source env/bin/activate && ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install -r requirements.txt && env/bin/linkenv env/lib/python2.7/site-packages gaenv && deactivate"'
      },
      regenWorkflow: {
        cmd: 'bash -c "source env/bin/activate && python WorkflowGenerate.py"'
      }
    },
    jsonlint: {
      workflow: {
        src: [ 'WorkflowSpecs/Workflow.*.json' ]
      },
      schema: {
        src: [ 'schema.json' ]
      }
    },
    json_schema: {
      test: {
        options: {},
        files: {
          'schema.json': []
        }
      }
    },
    // The actual grunt server settings
    connect: {
      options: {
        port: 9010,
        // Change this to '0.0.0.0' to access the server from outside.
        hostname: 'localhost',
        livereload: 35729
      },
      livereload: {
        options: {
          open: true,
          middleware: function (connect) {
            return [
              connect.static('.tmp'),
              connect.static('test'),
              connect().use(
                '/bower_components',
                connect.static('./bower_components')
              ),
              connect.static(appConfig.app)
            ];
          }
        }
      },
      test: {
        options: {
          port: 9001,
          middleware: function (connect) {
            return [
              connect.static('.tmp'),
              connect.static('test'),
              connect().use(
                '/bower_components',
                connect.static('./bower_components')
              ),
              connect.static(appConfig.app)
            ];
          }
        }
      },
      dist: {
        options: {
          open: true,
          base: '<%= yeoman.dist %>'
        }
      }
    },

    // Make sure code styles are up to par and there are no obvious mistakes
    jshint: {
      options: {
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      },
      all: {
        src: [
          'Gruntfile.js',
          '<%= yeoman.app %>/scripts/{,*/}*.js'
        ]
      },
      test: {
        options: {
          jshintrc: 'test/.jshintrc'
        },
        src: ['test/spec/{,*/}*.js']
      }
    },

    // Empties folders to start fresh
    clean: {
      python: [
        'gaenv',
        'env'
      ],
      dist: {
        files: [
          {
            dot: true,
            src: [
              '.tmp',
              '<%= yeoman.dist %>/{,*/}*',
              '!<%= yeoman.dist %>/.git*'
            ]
          }
        ]
      },
      server: '.tmp'
    },

    // Add vendor prefixed styles
    autoprefixer: {
      options: {
        browsers: ['last 1 version']
      },
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/styles/',
          src: '{,*/}*.css',
          dest: '.tmp/styles/'
        }]
      }
    },

    // Automatically inject Bower components into the app
    wiredep: {
      options: {
        cwd: '<%= yeoman.app %>'
      },
      app: {
        src: ['<%= yeoman.app %>/index.html'],
        ignorePath: /\.\.\//
      },
      sass: {
        src: ['<%= yeoman.app %>/styles/{,*/}*.{scss,sass}'],
        ignorePath: /(\.\.\/){1,2}bower_components\//
      }
    },




    // Compiles Sass to CSS and generates necessary files if requested
    compass: {
      options: {
        sassDir: '<%= yeoman.app %>/styles',
        cssDir: '.tmp/styles',
        generatedImagesDir: '.tmp/images/generated',
        imagesDir: '<%= yeoman.app %>/images',
        javascriptsDir: '<%= yeoman.app %>/scripts',
        fontsDir: '<%= yeoman.app %>/styles/fonts',
        importPath: './bower_components',
        httpImagesPath: '/images',
        httpGeneratedImagesPath: '/images/generated',
        httpFontsPath: '/styles/fonts',
        relativeAssets: false,
        assetCacheBuster: false,
        raw: 'Sass::Script::Number.precision = 10\n'
      },
      dist: {
        options: {
          generatedImagesDir: '<%= yeoman.dist %>/images/generated'
        }
      },
      server: {
        options: {
          debugInfo: true
        }
      }
    },

    // Renames files for browser caching purposes
    filerev: {
      dist: {
        src: [
          '<%= yeoman.dist %>/styles/{,*/}*.css',
          '<%= yeoman.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
          '<%= yeoman.dist %>/styles/fonts/*'
        ]
      }
    },


    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      dist: {
        files: [
          {
            expand: true,
            cwd: '<%= yeoman.app %>/images',
            src: '{,*/}*.{png,jpg,jpeg,gif}',
            dest: '<%= yeoman.dist %>/images'
          }
        ]
      }
    },
    svgmin: {
      dist: {
        files: [
          {
            expand: true,
            cwd: '<%= yeoman.app %>/images',
            src: '{,*/}*.svg',
            dest: '<%= yeoman.dist %>/images'
          }
        ]
      }
    },
    htmlmin: {
      dist: {
        options: {
          collapseWhitespace: true,
          conservativeCollapse: true,
          collapseBooleanAttributes: true,
          removeCommentsFromCDATA: true,
          removeOptionalTags: true
        },
        files: [
          {
            expand: true,
            cwd: '<%= yeoman.dist %>',
            src: ['*.html', 'views/{,*/}*.html'],
            dest: '<%= yeoman.dist %>'
          }
        ]
      }
    },

    ngAnnotate: {
      dist: {
        files: [
          {
            expand: true,
            // cwd: '<%= yeoman.app %>/scripts',
            src: '<%= yeoman.app %>/scripts/**/*.js',
            dest: '.tmp'
          }
        ]
      }
    },

    // Replace Google CDN references
    cdnify: {
      dist: {
        html: ['<%= yeoman.dist %>/*.html']
      }
    },

    copy: {
      dist: {
        files: [
          {
            expand: true,
            dot: true,
            cwd: '<%= yeoman.app %>',
            dest: '<%= yeoman.dist %>',
            src: [
              '*.{ico,png,txt}',
              '.htaccess',
              '*.html',
              'views/{,*/}*.html',
              'bower_components/**/*',
              'images/{,*/}*.{webp}',
              'fonts/*'
            ]
          },
          {
            expand: true,
            cwd: '.tmp/images',
            dest: '<%= yeoman.dist %>/images',
            src: ['generated/*']
          },
          {
            expand: true,
            cwd: '.',
            src: 'bower_components/bootstrap-sass-official/assets/fonts/bootstrap/*',
            dest: '<%= yeoman.dist %>'
          }
        ]
      },
      styles: {
        expand: true,
        cwd: '<%= yeoman.app %>/styles',
        dest: '.tmp/styles/',
        src: '{,*/}*.css'
      }
    },


    // Run some tasks in parallel to speed up the build process
    concurrent: {
      options: {logConcurrentOutput: true},
      server: [
        'compass:server'
      ],
      testSetup: [
        'compass'
      ],
      test: [
        'karma',
        'nose'
      ],
      dist: [
        'compass:dist',
        'imagemin',
        'svgmin',
        'jsonlint:workflow',
        'json_schema'
      ]
    },
    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: '<%= yeoman.app %>/index.html',
      options: {
        dest: '<%= yeoman.dist %>'
      }
    },

    // Performs rewrites based on filerev and the useminPrepare configuration
    usemin: {
      html: ['<%= yeoman.dist %>/{,*/}*.html'],
      css: ['<%= yeoman.dist %>/styles/{,*/}*.css'],
      options: {
        assetsDirs: ['<%= yeoman.dist %>', '<%= yeoman.dist %>/images']
      }
    },

    // Test settings
    karma: {
      unit: {
        configFile: 'karma.conf.js',
        singleRun: true
      }
    },
    bower: {
      app: {
        rjsConfig: '<%= yeoman.app %>/scripts/main.js',
        options: {
          exclude: ['requirejs', 'json3', 'es5-shim']
        }
      }
    },

    replace: {
      test: {
        src: '<%= yeoman.app %>/../test/test-main.js',
        overwrite: true,
        replacements: [
          {
            from: /paths: {[^}]+}/,
            to: function () {
              return require('fs').readFileSync(grunt.template.process('<%= yeoman.app %>') + '/scripts/main.js').toString().match(/paths: {[^}]+}/);
            }
          }
        ]
      }
    },

    // r.js compile config
    requirejs: {
      dist: {
        options: {
          dir: '<%= yeoman.dist %>/scripts/',
          modules: [
            {
              name: 'main'
            }
          ],
          preserveLicenseComments: false, // remove all comments
          removeCombined: true,
          baseUrl: '<%= yeoman.app %>/scripts',
          mainConfigFile: '.tmp/<%= yeoman.app %>/scripts/main.js',
          optimize: 'uglify2',
          uglify2: {
            mangle: false
          }
        }
      }
    }
  });

  grunt.registerTask('serve', 'Compile then start a connect web server', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['build', 'connect:dist:keepalive']);
    }

    grunt.task.run([
      'clean:server',
      'wiredep',
      'concurrent:server',
      'autoprefixer',
      'connect:livereload',
      'watch'
    ]);
  });
  grunt.registerTask('test', [
    'clean:server',
    'bower:app',
    'replace:test',
    'concurrent:testSetup',
    'autoprefixer',
    'connect:test',
    'concurrent:test'
  ]);

  grunt.registerTask('build', [
    'clean:dist',
    'wiredep',
    'bower:app',
    'replace:test',
    'useminPrepare',
    'concurrent:dist',
    'autoprefixer',
    'concat',
    'ngAnnotate',
    'copy:dist',
    'cdnify',
    'cssmin',
    'filerev',
    'usemin',
    'requirejs:dist',
    'htmlmin',
  ]);

  grunt.registerTask('default', [
    'newer:jshint',
    'test',
    'build'
  ]);
};

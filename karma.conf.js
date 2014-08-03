// Karma configuration

module.exports = function(config) {
  config.set({
    frameworks: ['jasmine', 'requirejs'],
    basePath: 'app',
    files: [
      'bower_components/angular/angular.js',
      '../test/main-test.js',
//      {pattern: 'app/lib/**/*.js', included: false},
      {pattern: '**/*.js', included: false},
      {pattern: 'views/*.html', included: false},
//      {pattern: '../test/**/*Spec.js', included: false},
//      'app/scripts/require-config.js'
//      'views/*.html'
    ],
//    exclude: [
//        'src/main.js'
//    ],
    browsers: ['PhantomJS'],
    port: 8010,
    singleRun: true,
    autoWatch: false,
    logLevel: config.LOG_DEBUG,
    preprocessors: {
      'views/*.html': ['ng-html2js']
    },
    ngHtml2JsPreprocessor: {
      // strip this from the file path
//      stripPrefix: 'base',
      enableRequireJs: true,
      // prepend this to the
//      prependPrefix: 'base/',

      // or define a custom transform function
//      cacheIdFromPath: function(filepath) {
//
//        return cacheId;
//      },

      // setting this option will create only a single module that contains templates
      // from all the files, so you can load them all with module('foo')
//      moduleName: 'foo'
    }
  });
};
var tests = [];
for (var file in window.__karma__.files) {
  if (window.__karma__.files.hasOwnProperty(file)) {
    if (/Spec\.js$/.test(file)) {
      tests.push(file);
    }
  }
}

requirejs.config({
    callback: window.__karma__.start,
    deps: tests,
    baseUrl: '/base',

  paths: {
    'jquery': 'bower_components/jquery/jquery',
    'bootstrap': 'bower_components/sass-bootstrap/dist/js/bootstrap',
    'angular': 'bower_components/angular/angular',
    'angular-resource':'bower_components/angular-resource/angular-resource',
    'angular-cookies':'bower_components/angular-cookies/angular-cookies',
    'angular-sanitize':'bower_components/angular-sanitize/angular-sanitize',
    'angular-route':'bower_components/angular-route/angular-route',
    'text': 'bower_components/requirejs-plugins/lib/text',
    'angular-form-builder': 'bower_components/angular-form-builder/dist/angular-form-builder',
    'angular-form-builder-components': 'bower_components/angular-form-builder/dist/angular-form-builder-components',
    'angular-validator': 'bower_components/angular-validator/dist/angular-validator',
    'angular-validator-rules': 'bower_components/angular-validator/dist/angular-validator-rules',
    'app': 'scripts/app',
    'text!/views/main.html': 'iews/main.html',
    'config/router': 'scripts/config/router',
    'controllers/main': 'scripts/controllers/main',
    'facebook': 'bower_components/angular-facebook/lib/angular-facebook',
  },
  shim: {
    'bootstrap' : {
      deps: ['jquery']
    },
    'angular': {
      deps: ['jquery'],
      exports: 'angular'
    },
    'angular-resource': ['angular'],
    'angular-route': ['angular'],
    'angular-cookies': ['angular'],
    'angular-sanitize': ['angular'],
    'angular-validator' : {
      deps: [
        'angular',
        'angular-validator-rules'
      ]
    },
    'facebook' : {
      deps: ['angular'],
      exports: 'fb'
    },
    'app' : ['angular', 'angular-resource', 'angular-route', 'bootstrap'],
    'angular-validator-rules' : ['angular'],
    'angular-form-builder-components' : ['angular'],
    'angular-form-builder' : {
      deps: [
        'angular-validator',
        'angular-form-builder-components',
        'angular',
        'jquery',
      ]
    }
  },
});
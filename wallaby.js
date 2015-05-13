module.exports = function () {
  return {
    files: [
      "api/**/*.coffee",
      "config/**/*.coffee",
      "assets/**/*.coffee",
      "tasks/**/*.coffee",
      "*.coffee"
    ],
    tests: [
      "test/**/*.spec.coffee"
    ],
    bootstrap: function (wallaby) {
      chai = require('chai');
      expect = chai.expect;
      chai.should();
      require('magic-globals');
      process.env.NODE_PATH = __base
      require('module').Module._initPaths();

    },
    env: {
      type: "node"
    }
  }
}

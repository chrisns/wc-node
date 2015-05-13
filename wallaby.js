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
      var chaiAsPromised = require("chai-as-promised");
      expect = chai.expect;
      chai.should();
      chai.use(chaiAsPromised);
      require('magic-globals');
      process.env.NODE_PATH = __base
      require('module').Module._initPaths();

    },
    env: {
      type: "node"
    },
    debug: true
  }
}
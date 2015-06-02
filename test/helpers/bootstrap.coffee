require 'magic-globals'
process.env.NODE_PATH = __base
require('module').Module._initPaths()

after (done) ->
  sails.lower done

before (done) ->
  this.timeout(15000)

  if global.sails
    return done()
  global.chai = require 'chai'
  chaiAsPromised = require 'chai-as-promised'
  global.expect = chai.expect
  global.chai.should()
  SailsOrientdbMochaHelper = require(__base + '/test/helpers/SailsOrientdbMochaHelper')
  chaiAsPromised = require 'chai-as-promised'
  global.chai.use chaiAsPromised
  global.chai.use SailsOrientdbMochaHelper
  global.chai.use require 'chai-things'
  freeport = require 'freeport'
  path = require 'path'
  fs = require 'fs'
  existsSync = fs.existsSync
  global.Promise = require 'bluebird'
  fs.existsSync = (filePath) ->
    if filePath and filePath.indexOf(path.join('instrumented', 'node_modules'))
      return true
    existsSync.apply this, arguments

  Sails = require 'sails'
  Barrels = require 'barrels'
  freeport (err, port) ->
    if err
      throw err
    global.sails = Sails.lift({
        hooks:
          grunt: false
        log:
          level: 'verbose'
        models:
          connection: 'test'
          migrate: 'drop'
        port: port
      }, (err) ->
      if err
        if err
          throw err
        return done()
      barrels = new Barrels
      fixtures = barrels.data
      barrels.populate (err) ->
        if err
          throw err
        return done()
    )

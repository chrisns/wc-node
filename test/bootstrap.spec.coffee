#Sails = require 'sails'
#Barrels = require 'barrels'
#require 'magic-globals'
##require 'should'
##require 'sails-memory'
## Global before hook
#chai = require('chai')
#chaiAsPromised = require('chai-as-promised')
#expect = chai.expect
#chai.should()
#chai.use chaiAsPromised
##require 'magic-globals'
##process.env.NODE_PATH = __base
##require('module').Module._initPaths()
##SailsOrientdbMochaHelper = require(__base + '/test/helpers/SailsOrientdbMochaHelper')
##chai.use SailsOrientdbMochaHelper
#
#before (done) ->
#  this.timeout(15000);
#
#  #  Sails.prototype.adapters['sails-memory'] = require 'sails-memory'
#  # Lift Sails with test database
#  Sails.lift {
##    adapters:
##      'sails-memory': require 'sails-memory'
#    log:
#      level: 'debug'
#    models:
#      connection: 'test'
#      migrate: 'drop'
#  }, (err, sails) ->
#    if err
#      return done(err)
#    # Load fixtures
#    barrels = new Barrels
#    # Save original objects in `fixtures` variable
#    fixtures = barrels.data
#    # Populate the DB
#    barrels.populate (err) ->
#      done err, sails
##  return null
## Global after hook
#after (done) ->
#  sails.lower done

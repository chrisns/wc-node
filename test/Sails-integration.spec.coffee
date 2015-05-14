#Sails = require('sails')
#sails = undefined
#
#describe 'Sails Integration', ->
#  before (done) ->
#    Sails.lift {
#      configuration: 'ff'
#      log: 'debug'
#    }, (err, server) ->
#      sails = server
#      if err
#        return done(err)
#      # here you can load fixtures, etc.
#      done err, sails
#  after (done) ->
## here you can clear fixtures, etc.
#    sails.lower done
#    return
#
#  it 'should do something', ->
#    expect sails
#    to.eql('test')
#

#Promise = require 'bluebird'
#Sails = require 'sails'
#
#
#  it 'should be able to lift the sales', ->
#    sails_promisified = Promise.promisify Sails.lift
#    #    globalSails = Sails()
#    #    mysails = Promise.promisify Sails.lift,
#    mysails = sails_promisified
##    mysails()
#    .tap (foo) ->
#      console.log(foo)
#
#    expect mysails
#    .to.and.eventually.be.satisfied
#
#  it 'should lift sails', (done) ->
#    sails_options =
#      log: 'info'
#      connections:
#        myLocalOrient:
#          database: 'wallaby'
#
#    Sails.load(sails_options, done)

describe 'Sails Integration', ->
  it 'should be able to lift the sails', ->
    expect(sails).to.be.an.object

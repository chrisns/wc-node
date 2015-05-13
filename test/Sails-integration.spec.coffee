Promise = require 'bluebird'
Sails = require 'sails'

describe 'Sails Integration', ->
  it 'should be able to lift the sales', ->
    sails_promisified = Promise.promisify Sails.lift
    #    globalSails = Sails()
    #    mysails = Promise.promisify Sails.lift,
    mysails = sails_promisified
#    mysails()
    .tap (foo) ->
      console.log(foo)

    expect mysails
    .to.and.eventually.be.satisfied

  it 'should lift sails', (done) ->
    sails_options =
      log: 'info'
      connections:
        myLocalOrient:
          database: 'wallaby'

    Sails.load(sails_options, done)

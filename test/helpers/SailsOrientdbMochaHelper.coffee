SailsOrientdbMochaHelper = (chai, utils) ->
  Assertion = chai.Assertion

  utils.addProperty Assertion.prototype, 'model', ->
    @assert typeof(@_obj) == 'object', 'expected #{this} to be a Model but got #{act}', 'expected #{this} to not be a Model', typeof(@_obj)


  utils.addProperty Assertion.prototype, 'vertex', ->
    @assert (@_obj.orientdbClass is undefined || @_obj.orientdbClass? is 'V' ), 'expected #{this} to be a Vertex ', 'expected #{this} to not be a Vertex'

  utils.addProperty Assertion.prototype, 'edge', ->
    @assert (@_obj.orientdbClass is 'E' ), 'expected #{this} to be an Edge ', 'expected #{this} to not be a Edge'

module.exports = SailsOrientdbMochaHelper

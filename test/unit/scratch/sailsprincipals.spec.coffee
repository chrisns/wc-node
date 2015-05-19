describe 'sails scratch playground', ->
  it 'should be able to create a workflow from the model', ->
    Workflow
    .create(
      foo: 'property'
    )
    .then (result) ->
      console.log result
    .catch (error) ->
      console.log error

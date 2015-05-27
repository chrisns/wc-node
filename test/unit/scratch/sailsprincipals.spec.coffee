describe 'sails scratch playground', ->
  it 'should be able to create a workflow from the model', ->
    promise = person.create({name: 'fooo'})
    .then (vertexes) ->
      promise = Promise.all [
        person.create({name: 'Bill'})
        person.create({name: 'John'})
        celebrity.create({name: 'my app'})
      ]
      .tap (vertexes) ->
        likes.create {person: vertexes[1].id, celebrity: vertexes[2].id, since: new Date()}
      .tap (vertexes) ->
        likes.create {person: vertexes[0].id, celebrity: vertexes[2].id, since: new Date()}
      .then (vertexes) ->
        Promise.all [
          person.find(vertexes[0].id).populate('celebrities')
          person.find(vertexes[1].id).populate('celebrities')
          celebrity.find(vertexes[2].id).populate('people')
        ]
      .tap console.log
    expect promise
    .to.eventually.be.ok

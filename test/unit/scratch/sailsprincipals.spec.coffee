describe 'sails scratch playground', ->
  it 'should be able to create a workflow from the model', ->
    promise = Promise.all [
      person.create({name: 'Bill'})
      person.create({name: 'John'})
      celebrity.create({name: 'Madona'})
    ]
    .tap (vertexes) ->
      likes.create {person: vertexes[1].id, celebrity: vertexes[2].id, since: new Date()}
    .tap (vertexes) ->
      likes.create {person: vertexes[0].id, celebrity: vertexes[2].id, since: new Date()}

    .then (vertexes) ->
      Promise.all [
        person.findOne(vertexes[0].id).populate('celebrities')
        person.findOne(vertexes[1].id).populate('celebrities')
        celebrity.findOne(vertexes[2].id).populate('people')
      ]
    .spread (person1, person2, celebrity) ->
      expect(person1).to.have.property 'name', 'Bill'

      expect person1.celebrities
      .to.include.one
      .and.have.property 'name', 'Madona'

      expect person2
      .to.have.property 'name', 'John'

      expect person2.celebrities
      .to.include.one
      .and.have.property 'name', 'Madona'

      expect(celebrity.name).to.eql 'Madona'

      expect celebrity.people
      .to.have.length 2
      .and.include.an.item.with.property 'name', 'Bill'
      .and.include.an.item.with.property 'name', 'John'

    expect promise
    .to.eventually.be.ok

  it 'should be able to create a chain of vertexes all joined together and efficiently query and join', ->
    to_make = _.range 0, 100
    vertexes = _.map to_make, (n) ->
      boy.create {name: 'boy ' + n}
    promise = Promise.all vertexes
    .tap (vertexes) ->
      edges = []
      _.forEach vertexes, (vertex, n) ->
        if n >= 1
          edges.push friends.create({boya: vertexes[n - 1].id, boyb: vertexes[n].id})
      Promise.all edges
    .then (vertexes) ->
      boy.find().populateAll()
    .tap console.log

    expect promise
    .to.eventually.be.ok

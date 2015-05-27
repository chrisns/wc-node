module.exports =
  tableName: 'likes'
  connection: 'testOrient'
  attributes:
    since: 'date'
    person:
      model: 'person'
      columnName: 'person'
    celebrity:
      model: 'celebrity'
      columnName: 'celebrity'

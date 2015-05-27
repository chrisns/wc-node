module.exports =
  tableName: 'friends'
  connection: 'testOrient'
  attributes:
    since: 'date'
    boya:
      model: 'boy'
      columnName: 'boya'
    boyb:
      model: 'boy'
      columnName: 'boyb'

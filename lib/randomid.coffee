FlakeIdGen = require('flake-idgen')
intformat = require('biguint-format')
generator = new FlakeIdGen


generate_id = ->
    return intformat(generator.next(), 'dec')

module.exports = generate_id
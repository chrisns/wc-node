var FlakeIdGen = require('flake-idgen');
var intformat = require('biguint-format');
var generator = new FlakeIdGen;


var generate_id = function() {
    return intformat(generator.next(), 'dec');
};
module.exports = generate_id;
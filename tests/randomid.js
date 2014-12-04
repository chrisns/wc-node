/*global describe, beforeEach, afterEach, it */
var randomId = require('../lib/randomid');
var chai = require("chai");
var chaiAsPromised = require("chai-as-promised");
var expect = chai.expect;

chai.use(chaiAsPromised);
chai.should();

describe('Random ID Generator', function () {

    it('Should be able to create an id with correct length', function () {
        var random_id = randomId();
        return expect(random_id).to.have.length.of(19);
    });

    it('Should be able to unique ids', function () {
        var random_id1 = randomId();
        var random_id2 = randomId();
        return expect(random_id1).to.not.equal(random_id2);
    });
});

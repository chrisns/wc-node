var prod = {};
var dev = {
    orient_db_config: {
        host: 'localhost',
        port: 2424,
        username: 'root',
        password: 'root'
    },
    orientdb_database: "wc_dev"
};

switch(process.env.NODE_ENV){
    case 'production':
        module.exports = prod;

    default:
        module.exports = dev;
}
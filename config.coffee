prod = {}
dev =
    orient_db_config:
        host: 'localhost'
        port: 2424
        username: 'root'
        password: 'root'
    orientdb_database: "wc_dev"

switch process.env.NODE_ENV
    when 'production' then module.exports = prod

    else
        module.exports = dev
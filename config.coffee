prod = {}
dev =
  orient_db_config:
    host: 'localhost'
    port: 2424
    username: 'root'
    password: 'root'
  orientdb_database: "wc_dev"


if process.env.NODE_ENV == 'production'
  module.exports = prod
else
  module.exports = dev

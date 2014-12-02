var express = require('express');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var orientdb = require("orientdb");
var Q = require("q");
var routes = require('./routes/index');
var users = require('./routes/users');

var app = express();
var hal = require("express-hal");
app.use(hal.middleware);
// view engine setup
//app.set('views', path.join(__dirname, 'views'));
//app.set('view engine', 'swig');


var dbConfig = {
    user_name: "root",
    user_password: "root",
    database_type: "graph",
    storage_type: "memory"
};
var serverConfig = {
    host: "localhost",
    port: 2424,
    user_name: "root",
    user_password: "root"
};

var server = new orientdb.Server(serverConfig);
var db = new orientdb.GraphDb("test", server, dbConfig);

//var db = new Db('test', server, dbConfig);

//var rename = Rx.Observable.fromCallback(server.connect);
//var server = server.connect();
//var db = db.create();
//console.log(db);

//function conn
//console.log(db.drop());
Q.ninvoke(server, 'connect')
    .then(function (sessionId) {
        console.log("Connected on session: " + sessionId);
    })
    .then(function () {
        return Q.ninvoke(db, 'drop');
    })
    .then(function () {
        return Q.ninvoke(db, 'create');
    })
    .done();
//Q.fcall(server.connect)
//.then(function(server) {
//    console.log(":a");
//}).catch(function(err) {
//        console.log(err);
//    })
//    .done();
//server.connect(function(err, sessionId) {
//
//    if (err) { console.log(err); }
//
//
//
//    db.create(function(err) {
//
//        //if (err) { console.log(err); return; }
//
//        console.log("Created database: " + db.databaseName);
//        console.log("gg");
//
//        db.drop(function(err) {
//            console.log("gg");
//            if (err) { console.log(err); return; }
//
//            console.log("Deleted database");
//
//            db.close(function(err) {
//
//                if (err) { console.log(err); return; }
//
//                console.log("Closed connection");
//            });
//        });
//    });
//});

// uncomment after placing your favicon in /public
//app.use(favicon(__dirname + '/public/favicon.ico'));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(require('stylus').middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/users', users);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;

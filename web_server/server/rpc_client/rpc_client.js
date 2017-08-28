var jayson = require('jayson');

// create a client connected to backend server
var client = jayson.client.http({
    port:4040,
    hostname: 'localhost'
});

// test RPC Method 
function add(a, b, callback){
    client.request('add', [a,b], function(err, error, response){
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}


module.exports = {
    add : add
};
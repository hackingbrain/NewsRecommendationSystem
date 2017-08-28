var client = require('./rpc_client');

// invoke add
client.add(2,3, function(response){
    console.assert(response === 5);
});
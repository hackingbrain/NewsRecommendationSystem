const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
    console.log('auth_checker: req: ' + req.headers);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }


    // get the last part from authorization header string like "bearer token-value"
    const token = req.headers.authorization.split(' ')[1];

    console.log('auth_checker: tocken: ' + token);

    // decode the tocken using a secret key-phase
    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        // the 401 code is for unauthorized status
        if (err) {
            return res.status(401).end();
        }

        const email = decoded.sub;

        // check if the user exists
        return User.findById(email, (userErr, user) => {
            if (userErr || !user){
                return res.status(401).end();
            }
            return next();
        });
    });
}
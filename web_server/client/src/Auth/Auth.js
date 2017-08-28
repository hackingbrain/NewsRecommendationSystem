class Auth {
    /**
     * Authentiate a user, save a token string to localStorage
     * @param {*} token 
     * @param {*} email 
     */
    static authenticateUser(token, email){
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);   
    }
    /**
     * Check if a user is authenticated
     */
    static isUserAuthenticated(){
        return localStorage.getItem('token') !== null;

    }

    
    /**
     * 
     */
    static deauthenticate(){
        localStorage.removeItem('token');
        localStorage.removeItem('email'); 
    }
    /**
     * Get token 
     */
    static getToken(){
        return localStorage.getItem('token');
    }

    static getEmail(){
        return localStorage.getItem('email');
    }
}

export default Auth;
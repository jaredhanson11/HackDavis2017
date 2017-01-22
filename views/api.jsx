
import Promise from 'promise-polyfill';
import fetch from 'whatwg-fetch';

function get(url) {
    return fetch(url)
        .then(response => {
            if(response.status >= 200 && response.status < 300) {
                return response
            } else {
                let error = new Error(response.statusText)
                error.response = response
                throw error
            }
        })
        .then(response=> response.json())
}

module.get = get;

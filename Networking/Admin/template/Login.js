const params = {
    "username": "admin",
    "password": "admin"
};
const options = {
    method: 'POST',
    body: JSON.stringify(params)
};
fetch('https://http://10.247.71.196:3000/login', options)
    .then(response => response.json())
    .then(response => {
        // Do something with response.
    });
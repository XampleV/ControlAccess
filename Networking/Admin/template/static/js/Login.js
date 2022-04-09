
function make_request(){
    const params = {
        "username": document.querySelector('uname').value,
        "password": document.querySelector('psw').value
    };

    
    const options = {
        method: 'POST',
        body: JSON.stringify(params)
    };
    fetch('https://http://10.247.71.196:3000/login', options)
        .then(response => response.json())
        .then(response => {
            console.log(response);
        });

}

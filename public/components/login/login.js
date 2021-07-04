document.getElementById('submit').addEventListener('click', async (e) => {
    e.preventDefault();

    let data = await axios.post('/api/auth', {username: document.getElementById('username').value, password: document.getElementById('password').value})
    let token = data.data;
    localStorage.setItem('user-token', token);
    localStorage.setItem('identity', JSON.stringify(JSON.parse(atob(token.split('.')[1]))));
    localStorage.setItem('expires', token.exp);
})
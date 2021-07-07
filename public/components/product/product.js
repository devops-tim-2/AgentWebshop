const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');

if (!id) window.location = '/notfound'

axios.get(`/api/product/${id}`).then(response => {
    let product = response.data;

    document.getElementById('name').innerHTML = `<a href="/shop?id=${product.catalog_id}"><h6 class="d-inline">Webshop</h6></a> <h6 class="d-inline"> > </h6> ${product.name}`;
    document.getElementById('price').innerHTML = `${product.price}$`;
    document.getElementById('available').innerHTML = `${product.available}/${product.quantity}`;
    document.getElementById('image').setAttribute('src', product.image_url);
    document.getElementById('add').addEventListener('click', (ev) => {
        ev.preventDefault();
        cart = JSON.parse(localStorage.getItem('cart')) || [];
        cart.push(product);
        localStorage.setItem('cart', JSON.stringify(cart));
        
        open_cart_content();
    })
})
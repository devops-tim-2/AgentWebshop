let inner = ''
    
cart = JSON.parse(localStorage.getItem('cart')) || [];

for (let product of cart) {
    inner += `<div class="col-12 my-1 d-flex justify-content-between">
                <span>
                        <table class="d-inline-block">
                            <tr>
                                <td rowspan="2">
                                    <img class="small-img" src="${product.image_url}">
                                </td>
                                <td>
                                    <div class="px-3 d-inline-block">${product.name}</div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <div class="px-3 d-inline-block">${product.price}$</div>
                                </td>
                            </tr>
                        </table>
                </span>
            </div>
            <hr>`
}

document.getElementById('cart-items').innerHTML = inner + `<h5 class="col-12 text-center">Total: ${Math.round(cart.map(e => e.price).reduce((a,b) => a+b) * 100) / 100}$ </h5>`;

document.getElementById('ordr').addEventListener('click', () => {
    axios.post('/api/order', {
        address: document.getElementById('address').value, 
        customer_name: document.getElementById('name').value,
        'order_items': cart.map(product => {
            return {
                'product_id': product.id,
                'quantity': 1
            }
        })
    }, bearer()).then(e => {
        localStorage.setItem('cart', '[]');
        window.history.back();
    });
})


function fill_cart_content() {
    let inner = ''
    
    cart = JSON.parse(localStorage.getItem('cart')) || [];

    for (let product of cart) {
        inner += `<div class="col-12 my-1 d-flex justify-content-between liajn">
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
                    <span>
                        <span class="btn btn-danger ml-5">Remove</span>
                    </span>
                </div>
                <hr>`
    }

    

    document.getElementById('cart-content').innerHTML = `<div class="scroller">${inner}</div><div class="btn btn-success col-6 offset-3 my-4">Checkout</div>`;
}


function open_cart_content() {
    fill_cart_content();
    document.getElementById('cart-content').style.display = 'block';
}

function close_cart_content() {
    document.getElementById('cart-content').style.display = 'none';
}

function flip_cart_content() {
    fill_cart_content();
    let cc = document.getElementById('cart-content');
    cc.style.display = cc.style.display == 'block' ? 'none' : 'block';
}
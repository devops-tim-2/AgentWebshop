const urlParams = new URLSearchParams(window.location.search);
const id = urlParams.get('id');

if (!id) window.location = '/notfound'


axios.get(`/api/catalog/${id}`).then(response => {
    let shop = response.data;

    document.getElementById('username').innerHTML = shop.owner;
    shop.products.forEach(product => {
        document.getElementById('row').innerHTML += `
        <div class="p-2 col-lg-3 col-md-4 col-sm-6 col-12">
            <div class="card p-0 col-12 cursor-pointer"  onclick="location.href='/product?id=${product.id}'">
                <h5 id="name" class="card-header">${product.name}</h5>
                
                <div class="card-body">
                    <img class="image" alt="Product image" class="col-12 d-block user-select-none" style="font-size:1.125rem;text-anchor:middle" src="${product.image_url}">
                    </img>
                </div>
                
                <div class="card-body">
                    <div class="d-flex justify-content-between">
                    <h6 class="card-title" id="price">${product.price}$</h6>
                    <h6 class="card-subtitle text-muted" id="available">${product.available} remaining</h6>
                    </div>
                </div>
            </div>
        </div>
        `
    });

    fill_cart_content()
})


// document.getElementById('tempadd').addEventListener('click', () => {
//     axios.post('/api/product', {'name': 'Jakna muska',
//     'price': 230,
//     'quantity': 30,
//     'image_url': 'https://www.intersport.rs/pub/media/catalog/product/cache/382907d7f48ae2519bf16cd5f39b77f9/1/2/1200068_icepeak_-jakna-m-poh-biggs_938.jpg'
// }, bearer()).then(res => console.log(res))
// })
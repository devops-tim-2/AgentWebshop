if (!localStorage.getItem('identity')) {
    window.location.href = '/login';
}
var global_image_link = '';

async function checkImage(url){
    if (url == '') return false;
     try {
         
        const res = await axios.get(url)
        return true;

     } catch (error) {
         return false;
     }

}

axios.get('/api/order', bearer()).then(async response => {
    let inner = ' <h1>Orders:</h1><div class="row">'
    for (let order of response.data.data) {
        for (let item of order.order_items) {
            item.item = (await axios.get(`/api/product/${item.product_id}`)).data
        }
    }
    response.data.data.forEach((e) => {
        inner += `
        <div class="col-2 border px-5 py-2">
            <p> <h4>Customer</h4> ${e.customer_name}</p>
            <p> <h4>Address</h4> ${e.address}</p> 
            <h4>Items:</h4>
            <ul>
                ${e.order_items.map(x => `<li><a href="/product?id=${x.item.id}">${x.item.name}</a></li>`).join(' ')}
            </ul>

            <h4>Total:</h4>
            <p>${e.order_items.map(y => y.item.price).reduce((a,b) => a+b)}$</p>
        </div>
        `
    });
    inner += '</div>'
    document.getElementById('orders').innerHTML = `
    <div><a class="btn btn-primary my-1" href="/shop?id=${JSON.parse(localStorage.getItem('identity')).catalog_id}">View shop</a></div>
    <hr>
    <form class="col-4">
        <label class="form-label">Name</label>
        <input class="form-control " id="name" type="text">

        <label class="form-label">Quantity</label>
        <input class="form-control " type="number" id="quantity">

        <label class="form-label">Price</label>
        <input class="form-control " type="number" id="price">

        <label class="form-label">Image</label>
        <input class="form-control " id="image" type="text">

        <img class="img-preview col-6 offset-3" src="" id="img-preview"></img>
    </form>
      <div class="btn btn-primary mb-5 mt-1" id="add">Add product to shop</div>
    ${inner}
    `;

    document.getElementById('image').addEventListener('input', async (event) => {
        let bsg = await checkImage(event.target.value);
        if (!bsg) {
            document.getElementById('img-preview').style.display = 'none';
            return;
        }
        let image_link = event.target.value;
        document.getElementById('img-preview').setAttribute('src', image_link)
        document.getElementById('img-preview').style.display = 'block';
    })

    document.getElementById('add').addEventListener('click', () => {
        axios.post('/api/product', {'name': document.getElementById('name').value,
        'price': +document.getElementById('price').value,
        'quantity': +document.getElementById('quantity').value,
        'image_url': document.getElementById('img-preview').getAttribute('src')
    }, bearer()).then(res => {
        document.getElementById('name').value = ''
        document.getElementById('price').value = 0
        document.getElementById('quantity').value = 0
        document.getElementById('image').value = ''
        document.getElementById('img-preview').style.display = 'none';
    })
    })
})
// Welcome Message

console.log("Food Delivery App Loaded");
let cartCount = 0;

    
    function renderCategories() {
      const list = document.getElementById('category-list');
      list.innerHTML = categories.map(c => `
        <li class="category-card">
          <a href="#${c.id}">
            <img src="${c.img}" alt="${c.name}">
            <h3>${c.name}</h3>
            <p>${c.desc}</p>
          </a>
        </li>
      `).join('');
    }

    
    function renderProducts() {
      const container = document.getElementById('product-list');
      container.innerHTML = products.map(p => `
        <div class="product-card">
          <img src="${p.img}" alt="${p.name}">
          <h3>${p.name}</h3>
          <p class="price">₹${p.price}</p>
          <button class="add-btn" onclick="addToCart(${p.id})">Add to Cart</button>
        </div>
      `).join('');
    }

    
    function addToCart(id) {
      cartCount++;
      document.getElementById('cart-count').textContent = cartCount;
      alert("Product added to cart!");
    }

    
    renderCategories();
    renderProducts();

// Login Validation

function validateLogin() {

    let email =
        document.getElementById("email").value;

    let password =
        document.getElementById("password").value;

    if(email === "" || password === ""){

        alert("Please fill all fields");

        return false;
    }

    return true;
}


// Register Validation

function validateRegister(){

    let name =
        document.getElementById("name").value;

    let email =
        document.getElementById("email").value;

    let password =
        document.getElementById("password").value;

    if(
        name === "" ||
        email === "" ||
        password === ""
    ){
        alert("All fields are required");
        return false;
    }

    return true;
}


// Add To Cart

function addToCart(foodName){

    alert(foodName + " added to cart");
}


// Place Order

function placeOrder(){

    alert("Order Placed Successfully");
}


// Delete Item

function deleteItem(itemName){

    let result =
        confirm(
            "Remove " +
            itemName +
            " from cart?"
        );

    if(result){

        alert(itemName + " removed");
    }
}
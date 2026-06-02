document.addEventListener("DOMContentLoaded", function () {

    let buttons = document.querySelectorAll(".add-cart");

    buttons.forEach(button => {
        button.addEventListener("click", function () {

            let itemName = this.dataset.name;

            let cart = JSON.parse(localStorage.getItem("cart")) || [];

            cart.push(itemName);

            localStorage.setItem("cart", JSON.stringify(cart));

            alert(itemName + " added to cart!");
        });
    });

});
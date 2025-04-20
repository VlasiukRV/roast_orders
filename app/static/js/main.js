(function () {

    document.addEventListener("DOMContentLoaded", () => {

        const cartContainer = document.getElementById("cart-container");
        const cartTotal = document.getElementById("cart-total");

        const cart = JSON.parse(localStorage.getItem("cart")) || [];
        let total = 0;

        function showNotification(message) {
            const notification = document.getElementById('notification');
            const messageElement = document.getElementById('notification-message');

            messageElement.textContent = message; // Устанавливаем сообщение в уведомление
            notification.classList.remove('hidden'); // Показываем уведомление

            // Через 3 секунды скрываем уведомление
            setTimeout(() => {
                notification.classList.add('hidden');
            }, 3000);
        }

        function saveCart() {
            localStorage.setItem("cart", JSON.stringify(cart));
        }

        function addToCart(name, price) {
            const existing = cart.find(item => item.name === name);
            if (existing) {
                existing.quantity += 1;
            } else {
                cart.push({name, price: parseFloat(price), quantity: 1});
            }

            saveCart();
            renderCart();
            showNotification(`${name} has been added to your cart!`);

        }

        document.querySelectorAll(".add-to-cart").forEach(btn => {
            btn.addEventListener("click", () => {
                const name = btn.dataset.name;
                const price = btn.dataset.price;
                addToCart(name, price);
            });
        });

        function renderCart() {
            cartContainer.innerHTML = "";
            total = 0; // Update the total amount when rendering the cart

            const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
            document.getElementById("item-count").textContent = `${totalItems} items`;

            if (cart.length === 0) {
                cartContainer.innerHTML = "<p>Your cart is empty. <a href='/shop'>Go to shop</a></p>";
                cartTotal.textContent = "0";
                saveCart();
                return;
            }

            cart.forEach((item, index) => {
                const itemTotal = item.price * item.quantity;
                total += itemTotal;

                const itemDiv = document.createElement("div");
                itemDiv.className = "flex justify-between items-center border-b pb-2";

                itemDiv.innerHTML = `
                    <div>
                        <p class="font-medium">${item.name}</p>
                        <p class="text-sm text-gray-600">${item.quantity} lb x $${item.price.toFixed(2)}</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button onclick="changeQuantity(${index}, -1)" class="px-2 py-1 bg-gray-200 rounded">−</button>
                        <span>${item.quantity}</span>
                        <button onclick="changeQuantity(${index}, 1)" class="px-2 py-1 bg-gray-200 rounded">+</button>
                        <button onclick="removeItem(${index})" class="ml-3 text-red-500">🗑</button>
                    </div>
                `;

                cartContainer.appendChild(itemDiv);
            });

            cartTotal.textContent = total.toFixed(2);
            saveCart();
        }

        window.changeQuantity = (index, delta) => {
            if ((cart[index].quantity + delta) >= 1) {
                cart[index].quantity += delta;
                renderCart();

                showNotification(`For ${cart[index].name} changed quantity!`);
            }
        };

        window.removeItem = (index) => {
            cart.splice(index, 1);
            renderCart();

            showNotification(`${cart[index].name} deleted!`);
        };

        renderCart();
    });

})();

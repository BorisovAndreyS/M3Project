document.addEventListener('DOMContentLoaded', function() {



    // --- Logic for the Main Page (home.html) ---
    const homePageContent = document.querySelector('.main-content-grid');
    if (homePageContent) {
        // 1. Sort Options Logic
        const sortButtons = document.querySelectorAll('.sort-options .sort-button');
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                sortButtons.forEach(btn => btn.classList.remove('active-sort'));
                this.classList.add('active-sort');
            });
        });

        // 2. Pagination Logic
        const paginationList = document.querySelector('.pagination-list');
        if (paginationList) {
            const paginationLinks = paginationList.querySelectorAll('.pagination__link');
            paginationLinks.forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    paginationLinks.forEach(lnk => lnk.classList.remove('active'));
                    this.classList.add('active');
                });
            });
        }

        // 3. Filter Logic (Keywords and Checkboxes)
        const keywordsList = document.querySelector('.keywords-list');
        const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');

        if (keywordsList && checkboxes.length > 0) {

            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    const keyword = this.dataset.keyword;
                    if (this.checked) {
                        if (!document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`)) {
                            const newTag = document.createElement('span');
                            newTag.className = 'keyword-tag';
                            newTag.setAttribute('data-keyword', keyword);
                            newTag.innerHTML = `${keyword} <i class="fa-solid fa-xmark remove-keyword-icon"></i>`;
                            keywordsList.appendChild(newTag);
                        }
                    } else {
                        const tagToRemove = document.querySelector(`.keyword-tag[data-keyword="${keyword}"]`);
                        if (tagToRemove) {
                            tagToRemove.remove();
                        }
                    }
                });
            });

            keywordsList.addEventListener('click', function(event) {
                const keywordIcon = event.target.closest('.remove-keyword-icon');
                if (keywordIcon) {
                    const keywordTag = keywordIcon.closest('.keyword-tag');
                    const keywordText = keywordTag.dataset.keyword;
                    const checkbox = document.querySelector(`.checkbox-container input[data-keyword="${keywordText}"]`);
                    if (checkbox) {
                        checkbox.checked = false;
                    }
                    keywordTag.remove();
                }
            });
        }
    }

    // --- Logic for Product Detail Pages (product-*.html) ---
    const productPageContent = document.querySelector('.page-product');
    if (productPageContent) {
        // Accordion
        const accordionTitle = document.querySelector('.accordion-title');
        if (accordionTitle) {
            accordionTitle.addEventListener('click', function() {
                this.closest('.accordion-item').classList.toggle('active');
            });
        }
        // "Add to Cart" Button and Counter
        const cartControls = document.querySelector('.cart-controls');
        if (cartControls) {
            const addToCartBtn = cartControls.querySelector('#add-to-cart-btn');
            const quantityCounter = cartControls.querySelector('#quantity-counter');
            const decreaseBtn = quantityCounter.querySelector('[data-action="decrease"]');
            const increaseBtn = quantityCounter.querySelector('[data-action="increase"]');
            const quantityValueSpan = quantityCounter.querySelector('.quantity-value');

            //Получаем текущее колво с сервера из data-атрибута или по умолчанию 0
            let quantity = parseInt(cartControls.dataset.quantity || 0);
            const productId = cartControls.dataset.productId;
            const productSlug = cartControls.dataset.productSlug;
            const addToCartUrl = cartControls.dataset.addCartUrl;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken')?.value;

            function updateView() {
                if (quantity === 0) {
                    addToCartBtn.classList.remove('is-hidden');
                    quantityCounter.classList.add('is-hidden');
                } else {
                    addToCartBtn.classList.add('is-hidden');
                    quantityCounter.classList.remove('is-hidden');
                    quantityValueSpan.textContent = `${quantity} in cart`;
                }
            }
            async function updateCartOnServer(newQuantity) {
                try {
                    const response = await fetch(addToCartUrl, {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ quantity: newQuantity})
                    });
                    if (!response.ok) throw new Error('Server error');

                    const data = await response.json();
                    if (data.success) {
                        quantity = data.quantity;
                        updateView();
                        return true;
                    }
                    return false;
                } catch (error) {
                        console.error('Full error:', error);
                        // Попробуем получить текст ошибки от сервера
                        if (error.response) {
                            error.response.text().then(text => {
                                console.error('Server response:', text);
                                alert('Ошибка сервера: ' + text);
                            });
                        } else {
                            alert('Не удалось обновить корзину. Проверьте консоль (F12).');
                        }
                        return false;
                    }
            }

            //Кнопка добавить в корзину
            addToCartBtn?.addEventListener('click', async function(e) {
                e.preventDefault();
                const success = await updateCartOnServer(1);
                if (success) {
                    console.log('✅ Товар добавлен');
                }
            });

            //Кнопка уменьшения кол-ва
            decreaseBtn?.addEventListener('click', async function() {
                if (quantity > 1) {
                    const newQty = quantity - 1;
                    const success = await updateCartOnServer(newQty);
                    if (!success) {
                        //Откат в случае ошибки
                        quantity = newQty + 1;
                        updateView();
                    }
                } else if (quantity === 1) {
                        const success = await updateCartOnServer(0);
                        if (success) {
                            console.log('✅ Товар удалён из корзины');
                        }
                    }
            });


            increaseBtn?.addEventListener('click', async function() {
                const newQty = quantity + 1;
                const success = await updateCartOnServer(newQty);
                if (!success) {
                    quantity = newQty - 1;
                    updateView();
                }
            });

            updateView();
        }
    }

//    Button add reviews
//    console.log('🔍 Кнопка:', document.getElementById('open-review-modal'));
//    console.log('🔍 Модалка:', document.getElementById('review-modal'));
    const modal = document.getElementById('review-modal');
    const openBtn = document.getElementById('open-review-modal');
    const closeBtn = document.querySelector('.close');
    const formModal = document.querySelector('#review-modal form');

    openBtn?.addEventListener('click', () => modal.classList.add('active'));
    closeBtn?.addEventListener('click', () => modal.classList.remove('active'));
    modal?.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.remove('active');
    });

    console.log('🔍 Form найдена:', formModal);
    if (formModal){
    formModal.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(formModal);
//    console.log('🔍 CSRF в formData:', formData.get('csrfmiddlewaretoken'));
    const response = await fetch(formModal.action, {
        method: 'POST',
        body: formData,

    });

    if (response.ok) {
//        console.log('✅ Успех!');
        modal.classList.remove('active');
        window.location.reload();
        // ← Обновить список отзывов на странице
    } else {
    console.error('❌ Ошибка:', response.status);
    }
    });
    }
    // Звёздный рейтинг
//    console.log('Звезд найдено!:', document.querySelectorAll('.star').length);

    document.querySelectorAll('.star-rating').forEach(container => {

        const input = container.querySelector('input[type="hidden"]');
//        console.log('🔍 Поиск .star-rating...');
        const starsContainer = container.querySelector('.stars');
//        console.log('starsContainer type:', typeof starsContainer, starsContainer);

        starsContainer?.addEventListener('click', (e) => {
//            console.log('🎯 Клик по:', e.target);
//            console.log('🎯 Классы:', e.target.classList);
            if (!e.target.classList.contains('star')){
//                console.log('❌ Клик не по звезде');
                return;
            }
            const value = e.target.dataset.value;
//            console.log('✅ Клик по звезде!', e.target.dataset.value);
            input.value = value;

            const allStars = container.querySelectorAll('.star');
            allStars.forEach(s => {
                const sVal = parseInt(s.dataset.value);
                const v = parseInt(value);
                s.classList.toggle('active', sVal <= v);
            });

            });

    });



    // --- Logic for Cart Page (cart.html) ---
    const cartPageContent = document.querySelector('.cart-page-wrapper');
    if (cartPageContent) {
        const cartItemsList = document.getElementById('cart-items-list');
        const cartTotalPriceElem = document.getElementById('cart-total-price');
        function updateCartTotal() {
//            console.log('Я тут!!!')
            let total = 0;
            document.querySelectorAll('.cart-item').forEach(item => {
                const priceText = item.querySelector('[data-item-total-price]').textContent;
                if (priceText) {
                    total += parseFloat(priceText.replace('$', ''));
                }
            });
            if (cartTotalPriceElem) cartTotalPriceElem.textContent = `$${total.toFixed(2)}`;
        }
        //Функция для обновления корзины на сервере об новом колве товара
        async function updateCartOnServer(itemId, newQuantity, updateUrl, csrfToken) {
                try {
                        const response = await fetch(updateUrl, {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ quantity: newQuantity,
                                               itemId: itemId })
                    });
                    if (!response.ok) throw new Error('Server error');

                    const data = await response.json();
                    if (data.success) {
                        quantity = data.quantity;
                        updateCartTotal();
                        return true;
                    }
                    return false;
                } catch (error) {
                        console.error('Full error:', error);
                        // Попробуем получить текст ошибки от сервера
                        if (error.response) {
                            error.response.text().then(text => {
                                console.error('Server response:', text);
                                alert('Ошибка сервера: ' + text);
                            });
                        } else {
                            alert('Не удалось обновить корзину. Проверьте консоль (F12).');
                        }
                        return false;
                    }
            }
        if (cartItemsList) {
            cartItemsList.addEventListener('click', async function(event) {
                const actionBtn = event.target.closest('[data-action]')
//                console.log('action-btn', actionBtn)
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken')?.value;
                if (!actionBtn) return;

                const action = actionBtn.dataset.action;
//                console.log('action', action)

                const cartItem = event.target.closest('.cart-item');
                if (!cartItem) return;


                const itemId = cartItem.dataset.itemid;
                const updateUrl = cartItem.dataset.updateUrl;
                //console.log('[updateUrl]', updateUrl);
                const quantityElem = cartItem.querySelector('.quantity-value-cart');
//                console.log('[.quantity-value-cart]', quantityElem);
                const itemTotalElem = cartItem.querySelector('[data-item-total-price]');
//                console.log('[data-item-total-price]', itemTotalElem);
                const basePrice = parseFloat(cartItem.dataset.price);
//                console.log('[cartItem.dataset.price]', basePrice);
                let quantity = parseInt(quantityElem.textContent);
                //console.log('let quantity', quantity)

//                if (event.target.closest('[data-action="increase"]')) {
//                    quantity++;
//                } else if (event.target.closest('[data-action="decrease"]')) {
//                    quantity = quantity > 1 ? quantity - 1 : 0;
//                }
//                if (event.target.closest('[data-action="remove"]') || quantity === 0) {
//                    cartItem.remove();
//                } else {

//                }


                //Получаем новое кол-во
                let newQty;
                if (action==='increase'){
                    newQty = quantity + 1;
                } else if (action ==='decrease'){
                    newQty = quantity - 1;
                } else if (action === 'remove'){
                    newQty = 0;
                }

                //Отправляем данные на сервер
                const success = await updateCartOnServer(itemId, newQty, updateUrl, csrfToken);

                if (success){
                      quantityElem.textContent = newQty;
//                      console.log("[newQty]", newQty)
                      itemTotalElem.textContent = `$${(basePrice * newQty).toFixed(2)}`;
                      if (newQty === 0){
                        cartItem.remove();
                    } else {
                        quantityElem.textContent = newQty;
                    }
                updateCartTotal();
                }
            });
        }
        updateCartTotal();
    }

    // --- Logic for Account and Admin Pages ---
    const accountAdminWrapper = document.querySelector('.account-page-wrapper, .admin-page-wrapper');
    if (accountAdminWrapper) {
        // Account Page Tabs
        const accountTabs = document.querySelectorAll('.account-tab');
        const tabPanes = document.querySelectorAll('.tab-pane');
        if (accountTabs.length > 0 && tabPanes.length > 0) {
            accountTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    accountTabs.forEach(item => item.classList.remove('active'));
                    tabPanes.forEach(pane => pane.classList.remove('active'));
                    const targetPane = document.querySelector(this.dataset.tabTarget);
                    this.classList.add('active');
                    if (targetPane) targetPane.classList.add('active');
                });
            });
        }

        // Admin Panel - Category Tags
        const categoryTagsContainer = document.querySelector('.category-tags');
        if (categoryTagsContainer) {
            categoryTagsContainer.addEventListener('click', function(e) {
                const clickedTag = e.target.closest('.category-tag');
                if (clickedTag) {
                    categoryTagsContainer.querySelectorAll('.category-tag').forEach(t => t.classList.remove('active'));
                    clickedTag.classList.add('active');
                }
            });
        }

        // Image Upload Simulation
        const uploadButton = document.getElementById('upload-image-btn');
        const fileInput = document.getElementById('image-upload-input');

        if (uploadButton && fileInput) {
            uploadButton.addEventListener('click', function() {
                fileInput.click();
            });

            fileInput.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    const placeholder = document.querySelector('.image-upload-placeholder');

                    reader.onload = function(e) {
                        placeholder.innerHTML = '';
                        placeholder.style.backgroundImage = `url('${e.target.result}')`;
                        placeholder.style.backgroundSize = 'cover';
                        placeholder.style.backgroundPosition = 'center';
                    }
                    reader.readAsDataURL(file);
                }
            });
        }
    }
});
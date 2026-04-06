% rebase('layout.tpl')
<!-- Вступительный блок с заголовком и описанием -->
<section class="intro">
    <h1>Новые поступления сезона</h1>
    <p>Подберите базовые вещи прямо на сайте. В наличии верхняя одежда, трикотаж и аксессуары.</p>
</section>

<!-- Секция с товарами -->
<section class="products">
    <h2>Товары</h2>
    <div class="product-grid">
        % for product in products:
        <!-- Карточка товара -->
        <article class="product-card">
            % if product.get('tag'):
            <span class="product-tag">{{product.get('tag')}}</span>
            % end
            <div class="product-image">
                <img src="/static/images/{{product.get('image')}}" alt="{{product.get('name')}}">
            </div>
            <h3>{{product.get('name')}}</h3>
            <p>{{product.get('description')}}</p>
            <strong>{{product.get('price')}}</strong>
        </article>
        % end
    </div>
</section>

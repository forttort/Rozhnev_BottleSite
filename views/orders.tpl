% rebase('layout.tpl')
<section class="inner-page orders-page">
    <h1 class="page-title">Оформленные заказы</h1>
    <p>Список заказов загружается из файла и обновляется после добавления новой записи.</p>

    % if success:
    <div class="form-message form-message-success">Заказ добавлен в список.</div>
    % end

    <form class="order-form" action="/orders" method="post" novalidate>
        <div class="form-field">
            <label for="order-number">Номер заказа</label>
            <input id="order-number" type="text" name="number" placeholder="MN-1001" value="{{form_data.get('number', '')}}">
            % if errors.get('number'):
            % for error in errors.get('number'):
            <span class="field-error">{{error}}</span>
            % end
            % end
        </div>

        <div class="form-field">
            <label for="order-description">Описание</label>
            <textarea id="order-description" rows="4" name="description" placeholder="Например: пальто и шарф, доставка курьером">{{form_data.get('description', '')}}</textarea>
            % if errors.get('description'):
            % for error in errors.get('description'):
            <span class="field-error">{{error}}</span>
            % end
            % end
        </div>

        <div class="form-row">
            <div class="form-field">
                <label for="order-date">Дата</label>
                <input id="order-date" type="text" name="date" placeholder="28.05.2026" value="{{form_data.get('date', '')}}">
                % if errors.get('date'):
                % for error in errors.get('date'):
                <span class="field-error">{{error}}</span>
                % end
                % end
            </div>
            <div class="form-field">
                <label for="order-phone">Телефон</label>
                <input id="order-phone" type="text" name="phone" placeholder="+7 (999) 123-45-67" value="{{form_data.get('phone', '')}}">
                % if errors.get('phone'):
                % for error in errors.get('phone'):
                <span class="field-error">{{error}}</span>
                % end
                % end
            </div>
        </div>

        <button class="btn btn-default" type="submit">Добавить</button>
    </form>
</section>

<section class="orders-section">
    <h2>Список заказов</h2>
    <div class="orders-list">
        % for order in orders:
        <article class="order-card">
            <div class="order-card-header">
                <strong>{{order.get('number')}}</strong>
                <span>{{order.get('date')}}</span>
            </div>
            <p>{{order.get('description')}}</p>
            <a href="tel:{{order.get('phone')}}">{{order.get('phone')}}</a>
        </article>
        % end
    </div>
</section>

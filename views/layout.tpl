<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maison Noir — магазин одежды</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <!-- Шапка сайта -->
    <header class="site-header">
        <div class="logo">Maison Noir</div>
        <nav class="site-nav">
            <a href="/">Главная</a>
            <a href="/about">О магазине</a>
            <a href="/contact">Контакты</a>
        </nav>
    </header>
    <!-- Основной контент подставляется через rebase -->
    <main class="page-content">
        {{!base}}
    </main>
    <!-- Низ -->
    <footer class="site-footer">
        <p>© Maison Noir, 2024</p>
    </footer>
</body>
</html>

# Social Web App - Frontend

React приложение для аутентификации и регистрации пользователей в стиле Medium.com.

## Возможности

- Страница авторизации (Login)
- Страница регистрации (Register)
- Дизайн в стиле Medium.com с serif-заголовками
- Валидация форм на клиенте
- Индикатор сложности пароля
- Анимации с Framer Motion
- Адаптивный дизайн (mobile, tablet, desktop)
- Доступность (ARIA, keyboard navigation)
- Интеграция с FastAPI backend через JWT

## Технологии

- React 18+
- React Router v6
- Framer Motion (анимации)
- Axios (HTTP клиент)
- Vite (сборщик)
- CSS Modules

## Установка

```bash
# Установка зависимостей
npm install

# Копирование .env файла
cp .env.example .env

# Запуск dev сервера
npm run dev

# Сборка для production
npm run build
```

## Структура проекта

```
frontend/
├── src/
│   ├── components/       # Переиспользуемые UI компоненты
│   │   ├── AuthLayout.jsx
│   │   ├── Button.jsx
│   │   ├── InputField.jsx
│   │   ├── PasswordInput.jsx
│   │   ├── SocialAuth.jsx
│   │   └── Divider.jsx
│   ├── pages/            # Страницы приложения
│   │   ├── LoginPage.jsx
│   │   └── RegisterPage.jsx
│   ├── styles/           # Глобальные стили
│   │   ├── index.css
│   │   └── animations.css
│   ├── utils/            # Утилиты
│   │   ├── api.js
│   │   └── validation.js
│   ├── App.jsx           # Главный компонент
│   └── main.jsx          # Точка входа
├── index.html
├── package.json
└── vite.config.js
```

## Дизайн-система

### Цвета
- Белый фон: `#FFFFFF`
- Чёрный текст: `#242424`
- Серый текст: `#6B6B6B`
- Зелёный акцент: `#1A8917`
- Границы: `#E6E6E6`
- Ошибки: `#C94A4A`

### Типографика
- Serif (заголовки): Noto Serif, GT Super, Georgia
- Sans-serif (интерфейс): System fonts

### Отступы (8px base)
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 44px
- 3xl: 56px

## API интеграция

Backend API работает на `http://localhost:8000/api/v1`

### Endpoints:
- `POST /auth/login` - Авторизация
- `POST /auth/register` - Регистрация
- `POST /auth/logout` - Выход
- `GET /auth/me` - Получить текущего пользователя

## Доступность

- Все формы имеют правильные `<label>`
- Поддержка навигации с клавиатуры (Tab, Shift+Tab, Enter)
- ARIA атрибуты для состояний ошибок
- Контрастность ≥ 4.5:1 (WCAG AA)
- Focus-visible для всех интерактивных элементов

## Браузеры

- Chrome/Edge (последние 2 версии)
- Firefox (последние 2 версии)
- Safari (последние 2 версии)

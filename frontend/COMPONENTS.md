# Документация компонентов

## UI Компоненты

### InputField
Универсальное текстовое поле ввода с поддержкой валидации.

**Props:**
- `label` - Название поля
- `type` - Тип input (text, email, etc.)
- `error` - Текст ошибки валидации
- `required` - Обязательное ли поле
- `className` - Дополнительные CSS классы

**Пример:**
```jsx
<InputField
  id="email"
  name="email"
  type="email"
  label="Email"
  placeholder="your@email.com"
  value={formData.email}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.email}
  required
/>
```

### PasswordInput
Поле ввода пароля с возможностью показа/скрытия и индикатором сложности.

**Props:**
- `label` - Название поля
- `error` - Текст ошибки валидации
- `showStrength` - Показывать ли индикатор сложности (default: false)
- `required` - Обязательное ли поле
- `className` - Дополнительные CSS классы

**Особенности:**
- Toggle видимости пароля (иконка глаза)
- 4 уровня сложности: слабый, средний, хороший, сильный
- Цветовая индикация: красный → оранжевый → желто-зелёный → зелёный

**Пример:**
```jsx
<PasswordInput
  id="password"
  name="password"
  label="Пароль"
  value={formData.password}
  onChange={handleChange}
  onBlur={handleBlur}
  error={errors.password}
  showStrength={true}
  required
/>
```

### Button
Универсальная кнопка с 3 вариантами стиля и состоянием загрузки.

**Props:**
- `variant` - Стиль: 'primary' | 'outlined' | 'ghost' (default: 'primary')
- `size` - Размер: 'small' | 'medium' | 'large' (default: 'medium')
- `type` - Тип кнопки: 'button' | 'submit' (default: 'button')
- `loading` - Состояние загрузки (показывает спиннер)
- `disabled` - Заблокирована ли кнопка
- `fullWidth` - Кнопка на всю ширину
- `className` - Дополнительные CSS классы

**Пример:**
```jsx
<Button
  type="submit"
  variant="primary"
  size="large"
  fullWidth
  loading={isLoading}
  disabled={isLoading}
>
  Войти
</Button>
```

### SocialAuth
Кнопки социальной авторизации (Google, GitHub).

**Особенности:**
- Outlined стиль
- Иконки социальных сетей
- Готово к интеграции OAuth

**Пример:**
```jsx
<SocialAuth />
```

### Divider
Горизонтальный разделитель с текстом посередине.

**Props:**
- `text` - Текст разделителя (default: 'или')

**Пример:**
```jsx
<Divider text="или" />
```

### AuthLayout
Layout-обёртка для страниц авторизации.

**Особенности:**
- Центрирование контента
- Карточка с тенью
- Логотип приложения
- Адаптивный дизайн
- Анимация появления (fade-in + slide-up)

**Пример:**
```jsx
<AuthLayout>
  <form>
    {/* Форма авторизации */}
  </form>
</AuthLayout>
```

## Страницы

### LoginPage
Страница авторизации пользователя.

**Особенности:**
- Валидация email и пароля
- Социальная авторизация
- Ссылка "Забыли пароль?"
- Ссылка на регистрацию
- Stagger-анимация полей формы
- Обработка ошибок сервера

**Маршрут:** `/login`

### RegisterPage
Страница регистрации нового пользователя.

**Особенности:**
- Поля: Имя, Email, Пароль, Подтверждение пароля
- Индикатор сложности пароля
- Чекбокс согласия с условиями
- Валидация совпадения паролей
- Социальная регистрация
- Ссылка на страницу входа
- Stagger-анимация полей формы

**Маршрут:** `/register`

### Dashboard
Защищённая страница после авторизации.

**Особенности:**
- Приветствие пользователя
- Отображение email и ID
- Кнопка выхода
- Автоматическая проверка токена
- Redirect на /login если не авторизован

**Маршрут:** `/dashboard`

## Утилиты

### validation.js
Функции валидации форм.

**Функции:**
- `validateEmail(email)` - Проверка email
- `validatePassword(password)` - Проверка пароля (min 8 символов)
- `validateName(name)` - Проверка имени (min 2 символа)
- `calculatePasswordStrength(password)` - Расчёт сложности пароля (0-4)

### api.js
API клиент для работы с backend.

**Функции:**
- `loginUser(credentials)` - Авторизация
- `registerUser(userData)` - Регистрация
- `logoutUser()` - Выход
- `getCurrentUser()` - Получить текущего пользователя

**Особенности:**
- Автоматическое добавление JWT токена в headers
- Автоматическое обновление токена при 401
- Обработка ошибок
- Axios interceptors

## Стили

### index.css
Дизайн-система и глобальные стили.

**CSS переменные:**
```css
--color-background: #FFFFFF
--color-text-primary: #242424
--color-text-secondary: #6B6B6B
--color-accent: #1A8917
--color-border: #E6E6E6
--color-error: #C94A4A

--font-serif: 'Noto Serif', Georgia, serif
--font-sans: System fonts

--spacing-sm: 8px
--spacing-md: 16px
--spacing-lg: 24px
--spacing-xl: 32px

--radius-sm: 4px
--radius-pill: 20px

--transition-fast: 0.15s ease
--transition-normal: 0.2s ease
```

### animations.css
Анимации в стиле Medium.

**Keyframes:**
- `fadeInUp` - Появление с подъёмом (0.4s)
- `fadeIn` - Простое появление (0.3s)
- `slideDown` - Слайд вниз (0.2s)

**Stagger классы:**
- `.stagger-1` до `.stagger-5` - Задержка для последовательной анимации

## Адаптивность

### Breakpoints
- **Mobile:** < 640px
- **Tablet:** 640px - 1024px
- **Desktop:** > 1024px

### Особенности
- Mobile: Карточка на 100% ширины, уменьшенные отступы
- Tablet: max-width 440px
- Desktop: max-width 480px с опциональной иллюстрацией

## Доступность

- Все поля имеют `<label>` с правильным `htmlFor`
- ARIA атрибуты для ошибок валидации
- `aria-invalid` для невалидных полей
- `role="alert"` для сообщений об ошибках
- Видимый `focus-outline` для всех интерактивных элементов
- Поддержка навигации клавиатурой (Tab, Shift+Tab, Enter)
- Контрастность ≥ 4.5:1 (WCAG AA)

## Анимации

### Принципы
- Сдержанные и плавные переходы
- Stagger-анимация для форм (0.08s между элементами)
- Fade-in с translateY для карточки (0.4s)
- Border-color transition для focus (0.2s)
- Hover эффекты (0.15s)

### Framer Motion
Используется для page-level анимаций:
- Появление карточки авторизации
- Stagger-анимация полей формы
- Cross-fade между страницами

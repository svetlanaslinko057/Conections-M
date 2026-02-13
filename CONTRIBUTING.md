# Contributing to FOMO Connections Module

## Начало работы

### Требования
- Node.js 18+
- Python 3.9+
- MongoDB 6+
- Yarn

### Локальная разработка

1. **Клонировать репозиторий**
```bash
git clone https://github.com/FOMOwiki/Conection-marge.git
cd Conection-marge
```

2. **Установить зависимости**
```bash
cd backend && yarn install
cd ../frontend && yarn install
```

3. **Настроить .env файлы**
```bash
# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=connections_db
PORT=8003

# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
```

4. **Запустить сервисы**
```bash
# Terminal 1: Node.js backend
cd backend && npx tsx src/app.ts

# Terminal 2: Python proxy
cd backend && python server.py

# Terminal 3: Frontend
cd frontend && yarn start
```

---

## Код-стайл

### TypeScript/JavaScript
- ESLint + Prettier
- Именование: camelCase для переменных, PascalCase для компонентов
- Async/await вместо callbacks

### React Components
- Функциональные компоненты с hooks
- Props destructuring
- data-testid для всех интерактивных элементов

### CSS/Tailwind
- Tailwind CSS для стилей
- Единый hover эффект: `hover:shadow-lg transition-shadow duration-300`
- Никаких inline styles (кроме динамических значений)

---

## Коммиты

Формат: `[type]: description`

Types:
- `feat:` — новая функциональность
- `fix:` — исправление бага
- `ui:` — изменения UI
- `docs:` — документация
- `refactor:` — рефакторинг
- `test:` — тесты

Примеры:
```
feat: add Reality Leaderboard page
fix: tooltip z-index on Early Signal page
ui: unify card hover animations
```

---

## Pull Requests

1. Создать branch от `main`
2. Внести изменения
3. Проверить линтинг: `yarn lint`
4. Создать PR с описанием изменений
5. Дождаться code review

---

## Тестирование

### Backend API
```bash
curl http://localhost:8001/api/health
curl http://localhost:8001/api/connections/clusters
```

### Frontend
- Визуальная проверка всех страниц
- Проверка tooltips, hover эффектов
- Проверка responsive на разных экранах

---

## Контакты

- FOMO Team

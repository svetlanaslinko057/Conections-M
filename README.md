# FOMO Connections Module

## Версия: 3.4.0

## Статус: ✅ Production Ready

---

## Описание

Модуль **Connections** — это система анализа связей и влияния в крипто-экосистеме. Отслеживает:

- Influencers и их сетевое влияние
- VC Funds и их портфели
- Co-investment паттерны
- Capital Flow между участниками рынка
- Reality Score — проверка достоверности прогнозов

---

## Архитектура

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HOST APPLICATION                             │
└────────┬───────────────────────────────────────────────────────────┘
         │ Port Adapters
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         PORTS LAYER                                  │
│  IExchangePort  IPricePort  ITelegramPort  IAlertPort               │
│  IOnchainPort   ISentimentPort  ITwitterLivePort  INotificationPort │
└────────┬───────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CONNECTIONS MODULE                               │
│  Unified Accounts │ Clusters │ Backers │ Graph │ Lifecycle          │
│  Reality Leaderboard │ Early Signal Radar │ Alt Season              │
└────────┬───────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 STORAGE (MongoDB - connections_*)                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| Node.js Fastify Backend | 8003 | Основной API сервер |
| Python FastAPI Proxy | 8001 | API proxy для Kubernetes |
| React Frontend | 3000 | Админка + UI |
| MongoDB | 27017 | База данных |

---

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/FOMOwiki/Conection-marge.git
cd Conection-marge
```

### 2. Установка зависимостей

```bash
# Backend
cd /app/backend && yarn install

# Frontend  
cd /app/frontend && yarn install
```

### 3. Настройка окружения

```bash
# Backend .env
MONGO_URL=mongodb://localhost:27017
DB_NAME=connections_db
PORT=8003
CONNECTIONS_MODULE_ENABLED=true
```

```bash
# Frontend .env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### 4. Запуск

```bash
# Через supervisor (production)
sudo supervisorctl restart backend frontend nodejs-backend

# Проверка health
curl http://localhost:8001/api/health
curl http://localhost:8001/api/v4/health
```

---

## API Endpoints

### Public API

| Endpoint | Описание |
|----------|----------|
| `GET /api/health` | Health check (proxy) |
| `GET /api/v4/health` | Health check (Node.js) |
| `GET /api/connections/unified` | Unified accounts (Influencers) |
| `GET /api/connections/clusters` | Influencer clusters |
| `GET /api/connections/backers` | VC Funds, Foundations |
| `GET /api/connections/opportunities` | Investment opportunities |
| `GET /api/connections/alt-season` | Alt season monitor |
| `GET /api/connections/lifecycle` | Asset lifecycle |
| `GET /api/connections/graph/v2` | Network graph |
| `GET /api/connections/reality/leaderboard` | Reality score leaderboard |

### Admin API

| Endpoint | Описание |
|----------|----------|
| `GET /api/admin/connections/backers` | Manage backers |
| `POST /api/admin/connections/backers` | Create backer |

---

## Frontend Pages

| URL | Описание |
|-----|----------|
| `/connections/influencers` | Карточки influencers |
| `/connections/clusters` | Cluster Attention - coordinated momentum |
| `/connections/backers` | VC Funds и Foundations |
| `/connections/backers/:slug` | Детальная страница backer |
| `/connections/graph` | Influence Network graph |
| `/connections/lifecycle` | Lifecycle Analytics |
| `/connections/alt-season` | Alt Season Monitor |
| `/connections/reality` | Reality Leaderboard |
| `/connections/radar` | Early Signal Radar |

---

## Supervisor Configuration

### Python Proxy (backend.conf)
```ini
[program:backend]
command=python /app/backend/server.py
directory=/app/backend
autostart=true
autorestart=true
```

### Node.js Backend (nodejs-backend.conf)
```ini
[program:nodejs-backend]
command=bash /app/backend/run-backend.sh
directory=/app/backend
autostart=true
autorestart=true
```

### Frontend (frontend.conf)
```ini
[program:frontend]
command=yarn start
directory=/app/frontend
autostart=true
autorestart=true
```

---

## Тестирование

### Health Check
```bash
curl http://localhost:8001/api/health
# Expected: {"status":"ok"}

curl http://localhost:8001/api/v4/health  
# Expected: {"status":"ok","module":"connections","version":"3.4.0"}
```

### API Test
```bash
curl http://localhost:8001/api/connections/clusters
curl http://localhost:8001/api/connections/lifecycle
```

---

## Структура файлов

```
/app/
├── backend/
│   ├── src/
│   │   ├── app.ts              # Main app entry
│   │   └── modules/
│   │       └── connections/    # Connections module
│   │           ├── ports/      # Port interfaces
│   │           ├── unified/    # Unified accounts
│   │           ├── clusters/   # Clusters
│   │           ├── backers/    # Backers
│   │           ├── graph-v2/   # Network graph
│   │           └── ...
│   ├── server.py               # Python FastAPI proxy
│   ├── run-backend.sh          # Node.js startup script
│   └── .env                    # Environment variables
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── connections/    # Connection pages
│       ├── components/
│       │   ├── ui/             # Shadcn UI components
│       │   └── ...
│       └── .env               # Frontend env
├── docs/
│   └── modules/
│       └── connections/        # Documentation
├── memory/
│   └── PRD.md                  # Product Requirements
└── README.md                   # This file
```

---

## UI/UX Features

- **Polished Design**: Градиенты, тени, анимации
- **Hover Effects**: Единый стиль `hover:shadow-lg transition-shadow`
- **Tooltips**: React Portal tooltips (не обрезаются overflow)
- **Dark/Light Theme**: Поддержка обеих тем
- **Responsive**: Адаптивный дизайн для всех экранов

---

## Недавние изменения (v3.4.0)

### UI Improvements
- ✅ Убраны "прыгающие" анимации чисел
- ✅ Унифицированы hover-эффекты карточек
- ✅ Исправлен z-index тултипов
- ✅ Убраны иконки "глазика" — тултипы при наведении
- ✅ Reality Leaderboard: понятный Verdict Mix (true/fake вместо C/X/N)
- ✅ Early Signal Radar: полный редизайн с Portal tooltips

### Bug Fixes
- ✅ Sample и Last Event отображаются в Reality Leaderboard
- ✅ Empty states на всех страницах
- ✅ Sort компонент выравнивание

---

## Контрольный вопрос

> Если удалить connections модуль — host продолжит работать?

**Ответ: ✅ ДА** — модуль полностью изолирован.

---

## Авторы

- FOMO Team

## Лицензия

Proprietary

---

**Last Updated:** 2026-02-14

# 🥤 Smoothie API

REST API на **Django + DRF + SQLite**. При первом `migrate` создаются таблицы и тестовые данные.

## 🚀 Запуск

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Swagger: <http://localhost:8000/api/docs/>

---

## 📝 Tasks

Решайте задачи в `smoothies/views.py` → `SmoothieViewSet`.

### Task 1: `GET /api/smoothies/`

Вернуть список всех смузи с вложенными ингредиентами.

### Task 2: `DELETE /api/smoothies/{id}/`

Удалить смузи.

_Требования:_

- Удалять можно только если статус `DRAFT`.
- Корректные HTTP-коды.
- Ингредиенты удаляются вместе со смузи (CASCADE в модели).

### Task 3: `GET /api/smoothies/{id}/nutrition/`

Посчитать калории через Fruityvice API (`GET https://www.fruityvice.com/api/fruit/{fruit_name}`).

_Требования:_

- Если фрукт не найден (404) — пропустить и продолжить расчёт.

### Task 4: AI-Assisted Debugging

`POST /api/smoothies/generate/?count=3` уже написан, но с багами. Должен: взять все фрукты из Fruityvice, выбрать `count` **уникальных** случайных, создать `DRAFT` смузи с ингредиентами.

---

## 📚 Links

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Fruityvice API](https://www.fruityvice.com/)

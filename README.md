# 🥤 Smoothie API - Live Coding Task

This is a partially completed REST API built with **Django, Django REST Framework, and SQLite**. The database automatically creates tables and seeds test data on first run.

## 🚀 How to Run

**Option 1: Docker (Recommended)**

```bash
docker build -t smoothie-api .
docker run --rm -p 8000:8000 -v .:/app smoothie-api
```

**Option 2: Python venv**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API Docs (Swagger UI): <http://localhost:8000/api/docs/>

---

## 📝 Tasks

_Note: The current architecture uses a Service Layer pattern with a basic `ViewSet`. However, you are completely free to refactor this and use DRF `ModelViewSet` or Mixins if you prefer the "DRF-way". Show us your best approach!_

### Task 1: `GET /api/smoothies/`

Return a list of all smoothies including their nested ingredients.

### Task 2: `DELETE /api/smoothies/{id}/`

Delete a smoothie.

_Requirements:_

- Only allow deleting if the status is `DRAFT`.
- Return correct HTTP status codes.
- Important: Ensure all associated ingredients are automatically deleted from the database.

### Task 3: `GET /api/smoothies/{id}/nutrition/`

Using AI, implement calorie calculation with Fruityvice API (`GET https://www.fruityvice.com/api/fruit/{fruit_name}`).

_Requirements:_

- If fruit is not found (404), skip it and continue calculation.

### Task 4: AI-Assisted Debugging

The endpoint `POST /api/smoothies/generate/?count=3` is **already implemented** but contains bugs. It should fetch all available fruits from the Fruityvice API, pick `count` unique random fruits, and create a new `DRAFT` smoothie with those fruits as ingredients.

Use any AI tool to find and fix all the issues. We want to see how you work with AI — your prompts, reasoning, and how you validate the suggestions.

---

## 📚 Useful Links

- **Django REST Framework Docs:** https://www.django-rest-framework.org/
- **Django ORM & Database:** https://docs.djangoproject.com/en/4.2/topics/db/
- **Django-Filter Integration:** https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
- **Requests Docs:** https://requests.readthedocs.io/en/latest/
- **Python ThreadPoolExecutor:** https://docs.python.org/3/library/concurrent.futures.html
- **Fruityvice API:** https://www.fruityvice.com/

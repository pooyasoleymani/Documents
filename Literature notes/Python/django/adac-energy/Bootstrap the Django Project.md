---
Created Date: 2026-08-22
---
---


The goal of this step is to create a **production-oriented foundation**, not just a Django demo.

---

## 10.1 Repository

Create:

```text
adac-energy/
```

Initial structure:

```text
adac-energy/
├── apps/
├── config/
├── templates/
├── static/
├── media/
├── tests/
├── docs/
├── docker/
├── scripts/
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── pyproject.toml
└── README.md
```

---

# 10.2 Python environment

Use Python 3.13+ for the project.

I recommend `uv` for dependency and environment management.

```bash
mkdir adac-energy
cd adac-energy

uv init

uv python install 3.13
uv python pin 3.13
```

Install Django and the initial dependencies:

```bash
uv add django psycopg[binary] pillow
```

Development/testing:

```bash
uv add --dev pytest pytest-django ruff mypy
```

We'll add other dependencies only when we actually need them.

---

# 10.3 Create Django project

```bash
uv run django-admin startproject config .
```

You should now have:

```text
adac-energy/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── manage.py
```

We'll restructure `settings.py` shortly.

---

# 10.4 Create application modules

Create the initial domains:

```bash
mkdir -p apps
touch apps/__init__.py
```

Then:

```bash
uv run python manage.py startapp core apps/core
uv run python manage.py startapp catalog apps/catalog
uv run python manage.py startapp solutions apps/solutions
uv run python manage.py startapp industries apps/industries
uv run python manage.py startapp knowledge apps/knowledge
uv run python manage.py startapp projects apps/projects
uv run python manage.py startapp brands apps/brands
uv run python manage.py startapp quotes apps/quotes
uv run python manage.py startapp accounts apps/accounts
```

Result:

```text
apps/
├── __init__.py
│
├── core/
├── catalog/
├── solutions/
├── industries/
├── knowledge/
├── projects/
├── brands/
├── quotes/
└── accounts/
```

---

# 10.5 Don't use one huge models.py

For the catalog, immediately create:

```text
apps/catalog/
├── __init__.py
├── admin/
│   └── __init__.py
├── models/
│   ├── __init__.py
│   ├── category.py
│   ├── product.py
│   ├── variant.py
│   ├── specification.py
│   ├── image.py
│   ├── document.py
│   └── relationship.py
├── services/
│   ├── __init__.py
│   └── product_service.py
├── views/
│   ├── __init__.py
│   └── product.py
├── tests/
│   └── __init__.py
├── urls.py
└── apps.py
```

This is preferable to eventually having:

```text
models.py → 2,000 lines
views.py  → 1,500 lines
```

---

# 10.6 Settings architecture

Change:

```text
config/
└── settings.py
```

to:

```text
config/
└── settings/
    ├── __init__.py
    ├── base.py
    ├── development.py
    └── production.py
```

Move common settings into:

```text
config/settings/base.py
```

Development-specific configuration goes into:

```text
development.py
```

Production-specific configuration goes into:

```text
production.py
```

This gives us:

```text
development
     │
     ▼
base + development settings


production
     │
     ▼
base + production settings
```

---

# 10.7 Environment variables

Create:

```text
.env.example
```

```env
DJANGO_SETTINGS_MODULE=config.settings.development

SECRET_KEY=change-me
DEBUG=True

POSTGRES_DB=adac
POSTGRES_USER=adac
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

ALLOWED_HOSTS=localhost,127.0.0.1
```

Never commit the real `.env`.

`.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]

media/
staticfiles/

.pytest_cache/
.mypy_cache/
.ruff_cache/

.idea/
.vscode/
```

---

# 10.8 PostgreSQL

For development:

```yaml
services:
  postgres:
    image: postgres:18
    container_name: adac-postgres
    restart: unless-stopped

    environment:
      POSTGRES_DB: adac
      POSTGRES_USER: adac
      POSTGRES_PASSWORD: adac

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql

volumes:
  postgres_data:
```

Start it:

```bash
docker compose up -d postgres
```

Check:

```bash
docker compose ps
```

---

# 10.9 Why PostgreSQL from day one?

Don't start with SQLite and migrate later.

Our application needs:

- relational data
    
- product relationships
    
- specifications
    
- filtering
    
- full-text/search capabilities
    
- transactions
    
- indexes
    
- constraints
    

PostgreSQL is the correct foundation.

---

# 10.10 Django database configuration

In `base.py`:

```python
import os


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}
```

Later we can use a typed environment configuration library, but don't add abstraction unnecessarily yet.

---

# 10.11 Installed apps

Add:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "apps.core",
    "apps.catalog",
    "apps.solutions",
    "apps.industries",
    "apps.knowledge",
    "apps.projects",
    "apps.brands",
    "apps.quotes",
    "apps.accounts",
]
```

---

# 10.12 Media configuration

Products will have:

```text
images
PDFs
CAD files
certificates
manuals
```

Configure:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Development URL:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
```

Production will eventually use object storage rather than serving media through Django.

---

# 10.13 Static files

```python
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

So:

```text
static/
├── css/
├── js/
├── images/
└── icons/
```

---

# 10.14 Base template

Create:

```text
templates/
└── base.html
```

Initial structure:

```html
<!DOCTYPE html>
<html
    lang="{{ LANGUAGE_CODE }}"
    dir="{% if LANGUAGE_CODE == 'fa' %}rtl{% else %}ltr{% endif %}"
>
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        {% block title %}
            ADAC Energy
        {% endblock %}
    </title>

    {% block meta %}
    {% endblock %}

    {% block styles %}
    {% endblock %}
</head>

<body>

    {% include "components/header.html" %}

    <main>
        {% block content %}
        {% endblock %}
    </main>

    {% include "components/footer.html" %}

    {% block scripts %}
    {% endblock %}

</body>
</html>
```

This becomes the root of the frontend.

---

# 10.15 Component directory

Create:

```text
templates/
├── base.html
│
├── components/
│   ├── header.html
│   ├── footer.html
│   ├── button.html
│   ├── breadcrumb.html
│   ├── product_card.html
│   ├── document_card.html
│   └── modal.html
│
└── pages/
    └── home.html
```

The important principle:

> **Pages compose components. Components should not contain page-specific business logic.**

---

# 10.16 Design tokens

Our primary agency color is:

```text
#5E1945
```

We'll make it a first-class design token.

Conceptually:

```css
:root {
    --color-primary: #5E1945;

    --color-primary-dark: #421331;
    --color-primary-light: #7A285B;

    --color-text: #151515;
    --color-text-muted: #666666;

    --color-background: #FFFFFF;
    --color-background-soft: #F7F7F7;

    --color-border: #E5E5E5;
}
```

The important point is that we **do not sprinkle `#5E1945` everywhere**.

Instead:

```css
var(--color-primary)
```

This makes the design system maintainable.

---

# 10.17 Brand color usage

The burgundy should dominate important interaction points:

```text
Primary CTA
Active navigation
Important headings
Selected filters
Product highlights
Links
Focus states
```

But don't make the entire website burgundy.

The visual hierarchy should be approximately:

```text
White / light neutral
        ↓
Dark typography
        ↓
Burgundy accent
        ↓
Images / technical diagrams
```

This keeps the website industrial rather than looking like a marketing brochure.

---

# 10.18 Frontend animation strategy

We'll use three levels.

### Level 1 — CSS

For:

```text
hover
focus
buttons
cards
navigation
```

Example:

```css
.button {
    transition:
        transform 180ms ease,
        background-color 180ms ease;
}

.button:hover {
    transform: translateY(-2px);
}
```

### Level 2 — Alpine.js

For:

```text
mobile menu
accordion
modal
gallery
dropdown
```

### Level 3 — GSAP

Only for major visual storytelling:

```text
Homepage hero
Industrial diagrams
Large section transitions
Product showcase
```

We should **not animate every element**.

Industrial websites need to communicate technical information quickly.

---

# 10.19 HTMX

Add HTMX to the base template.

Then our frontend can perform:

```text
Search
Filtering
Pagination
Variant selection
Quote form
```

without turning the website into a SPA.

Architecture:

```text
Browser
   │
   │ HTMX
   ▼
Django View
   │
   ▼
Partial Template
   │
   ▼
DOM update
```

---

# 10.20 First milestone

After this step, our application should be able to do:

```text
$ docker compose up -d

$ uv run python manage.py migrate

$ uv run python manage.py runserver
```

and show:

```text
┌──────────────────────────────────────┐
│ ADAC ENERGY                          │
│                                      │
│ Products   Solutions   Industries    │
│                                      │
│                                      │
│         WEBSITE FOUNDATION           │
│                                      │
│                                      │
│              #5E1945                 │
│                                      │
└──────────────────────────────────────┘
```

No catalog yet.

That's intentional.

First we establish the foundation.

---

# 10.21 Then the first real implementation

Our next implementation milestone should be:

```text
STEP 11
        │
        ├── Category model
        ├── Product model
        ├── Brand model
        ├── SpecificationDefinition
        ├── ProductSpecification
        ├── ProductImage
        ├── ProductDocument
        ├── ProductVariant
        ├── ProductRelationship
        │
        ├── Django migrations
        ├── Django Admin
        │
        └── Create first real product
```

The critical target is this:

> **Before we build the public product UI, an administrator should be able to log into Django Admin and create a complete product—including images, technical specifications, variants and PDF documents.**

Once that works, the frontend becomes a presentation layer over a real content system rather than a collection of hard-coded pages.
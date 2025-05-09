# Trashify API

> Built with passion, despair, and questionable time management.  
> Worth: **4 points**  
> Effort: **All of my remaining will to live**

Backend service for scanning, categorizing, and tracking waste items based on images. Built on Django + DRF with a hexagonal architecture, using PostgreSQL and MinIO for storage.

## 📦 What This Project Does (Allegedly)

- User uploads photo of trash.
- App says: "bro, that's plastic. 300g of it. Recyclable."
- User pretends to care and edits details if they feel like it.
- Data gets saved for *statistics* nobody will ever check.
- That's it. That's the dream.


## Setup Instructions

Because nothing says "easy setup" like 15 tools duct-taped together, here’s how to get started:

### 1. Clone the Repository
```bash
git clone https://github.com/bcastillo-2022474/waste-classifier-api.git
cd waste-classifier-api
```

---

### 2. Configure Environment Variables
Create a `.env` file by copying the provided example:
```bash
touch .env
cp .env.example .env
```
Then, **update** the `.env` with your own MinIO access/secret keys after setting up the MinIO bucket (see MinIO setup section below if you like doing things out of order).

---

### 3. Start Services with Docker
You’ll need [Docker installed](https://docs.docker.com/engine/install/).  
Once it’s up and running:
```bash
docker compose up -d
```
This will launch:
- PostgreSQL (because your data deserves a home)
- MinIO (because cloud storage sounds fancy)

---

### 4. Install Python Dependencies
You’ll need [Poetry](https://python-poetry.org/docs/) for dependency management.  
Install it first:
```bash
pip install poetry
```

Then install project dependencies:
```bash
poetry install
```

**Important**:  
You'll also need `dotenv-cli` to load environment variables when running Django commands:
```bash
pip install python-dotenv[cli]
```

---

### 5. Create a Virtual Environment (Optional but Highly Recommended)
If you like isolation (emotionally and technically):
```bash
python -m venv .venv
source .venv/bin/activate
```
> On Windows or other exotic operating systems, activating the environment will be slightly different. Good luck.

---

### 6. Apply Database Migrations
Prepare your database for disappointment:
```bash
dotenv -f .env run -- python api/manage.py migrate
```

---

### 7. Create a Superuser
Because you'll need to log in *somehow*:
```bash
dotenv -f .env run -- python api/manage.py createsuperuser
```

---

### 8. Run the Development Server
Finally:
```bash
dotenv -f .env run -- python api/manage.py runserver
```

The server should now be live at `http://localhost:8000/`.  
(If it's not... well, join the club.)

---

## MinIO Setup (DON’T SKIP THIS)
You’ll need to:
1. Access the MinIO Console at [http://localhost:9001](http://localhost:9001)
2. Log in with the credentials from `.env`
3. Create a new **bucket** (e.g., `waste-item`)
4. Generate Access and Secret Keys
5. Update your `.env` file with the correct keys:
   ```bash
   AWS_ACCESS_KEY_ID=your-new-key
   AWS_SECRET_ACCESS_KEY=your-new-secret
   ```

Because nothing screams “modern backend” like copying random keys between UIs.

---

## Hexagonal Architecture (a.k.a. Why We Made This Complicated)

This project follows **Hexagonal Architecture** (Ports and Adapters pattern):

- **Core Logic**:  
  Found in the `core/` directory — totally unaware that your database, file storage, or API even exist.  
- **Infrastructure Layer**:  
  Found in the `api/` directory — handles Django, REST, storage, authentication, and telling the core what to do.
  (Translation: You can replace the database, storage, or framework later without too many tears.)

The basic idea is:  
> We built a beautiful library and then bolted a web server onto it like a sad Lego set.

---

## Project Structure (Quick Tour for the Lost)
```
.
├── api/       # Django project: views, serializers, models
├── core/      # Application logic: use cases, entities, ports
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md  # You're here
```

---

# 🪦 Known Issues

- Setup might randomly explode if you breathe wrong.
- Rate-limiting? HAHAHA no. (OpenAI might make me poor lmao)
- Abuse protection? What's that?
- Works best if nobody uses it.
- Built for Linux.  
  Windows users? May God have mercy on your souls. I use arch btw


---

# 🔄 Waste Item Flow (Dumb Diagram Version)

Here's a *very professional* ASCII diagram of how waste classifier logic flows:

```
User
  ↓
Takes Photo
  ↓
Photo Uploaded → [Scan Waste Item Use Case]
                        ↓
        [Detect Material, Weight, Category]
                        ↓
        Pre-populate Form with Detected Data
                        ↓
        User Edits/Confirms → [Save Waste Item Use Case]
                        ↓
             Store in DB + MinIO Storage
                        ↓
    Data Available for Listing, Stats, Etc
```

---

## Final Notes

> [!WARNING]  
> This setup was designed to be as *compatible* as possible across shells and OSes.  
> It has NOT been deeply tested on Windows, BSD, microwaves, or cursed Linux distros.  
> **Good luck, brave soul.**

---

# ✌️ Thanks for Reading

If you actually read this whole README, you’re legally required to give me the whole score.

**– Built by Joao Castillo, a ton of misplaced ambition, and another 4 guys whos names are not Relevant -**

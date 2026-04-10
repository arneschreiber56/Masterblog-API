Masterblog API

A simple RESTful API for managing blog posts, built with Flask.
This project focuses on backend development, including API design, validation, rate limiting, and documentation via Swagger UI.

⸻

🚀 Features
	•	Create, update, and delete blog posts
	•	Retrieve all posts
	•	Search posts by title and/or content
	•	Sort posts (by title or content, ascending/descending)
	•	Rate limiting (Flask-Limiter)
	•	CORS enabled
	•	Interactive API documentation (Swagger UI)

⸻

📁 Project Structure

backend/
├── backend_app.py
├── requirements.txt
├── static/
│   └── masterblog.json
└── masterblog_backend.log

frontend/ (preliminary)
├── frontend_app.py
├── static/
│   ├── main.js
│   └── styles.css
└── templates/
└── index.html

⸻

⚙️ Setup

1. Clone repository

git clone 
cd 

2. Create virtual environment

python3 -m venv venv
source venv/bin/activate

(Windows: venv\Scripts\activate)

3. Install dependencies

pip install -r backend/requirements.txt

4. Run backend

cd backend
python backend_app.py

Server runs on:
http://127.0.0.1:5002

⸻

📚 API Documentation

Swagger UI is available at:

http://127.0.0.1:5002/api/docs

You can explore and test all endpoints directly in the browser.

⸻

🔌 API Endpoints

Posts

GET /api/posts
→ Returns all posts (supports optional sorting)

POST /api/posts
→ Creates a new post

PUT /api/posts/{post_id}
→ Updates an existing post

DELETE /api/posts/{post_id}
→ Deletes a post

⸻

Search

GET /api/posts/search?title=&content=
→ Searches posts by title and/or content

⸻

Sorting

GET /api/posts?sort=title&direction=asc
GET /api/posts?sort=content&direction=desc

⸻

⚠️ Notes
	•	This project uses in-memory storage (no database)
	•	Data is reset on server restart
	•	Focus is on backend/API design rather than persistence

⸻

🛠️ Tech Stack
	•	Python 3
	•	Flask
	•	Flask-CORS
	•	Flask-Limiter
	•	Swagger UI (flask-swagger-ui)

⸻

📌 Future Improvements
	•	Add database (e.g. SQLAlchemy)
	•	Implement pagination
	•	Add GET /api/posts/{id}
	•	Improve validation layer
	•	Add unit tests (pytest)
	•	Refactor into modular backend structure

⸻

👨‍💻 Author

Arne
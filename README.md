# 🚀 Mini Project 2: Smart Task Manager API

## 📌 Overview

In this assignment, you will build a **Task Management Backend Application** using **FastAPI**.

The goal is to design and implement a clean, well-structured backend system that allows users to create, manage, and interact with tasks through a RESTful API — along with a simple frontend interface.

This project is designed to reinforce your understanding of:

* REST APIs
* FastAPI
* HTTP methods
* Data validation
* Testing
* Templating & static resources

---

## 🎯 Objectives

By completing this project, you should be able to:

* Design and implement RESTful APIs using FastAPI
* Handle data validation and error handling properly
* Work with query parameters and filtering
* Write automated tests for your API
* Integrate backend logic with a simple frontend (HTML templates or static pages)
* Structure your code in a clean and maintainable way

---

## 🧱 Project Requirements

### 1. Task Model

Each task should have the following structure:

```json
{
  "id": int,
  "title": string,
  "description": string,
  "status": "todo" | "in_progress" | "done",
  "priority": "low" | "medium" | "high",
  "tags": [string],
  "created_at": datetime
}
```

⚠️ Important:

* You must **store data in memory** (e.g., Python list or dictionary)
* Do NOT use any database

---

### 2. API Endpoints

You must implement the following endpoints:

| Method | Endpoint      | Description                  |
| ------ | ------------- | ---------------------------- |
| POST   | `/tasks`      | Create a new task            |
| GET    | `/tasks`      | Get all tasks (with filters) |
| GET    | `/tasks/{id}` | Get a single task by ID      |
| PUT    | `/tasks/{id}` | Update a task                |
| DELETE | `/tasks/{id}` | Delete a task                |

---

### 3. Filtering & Search

The `/tasks` endpoint must support filtering using query parameters:

Examples:

```
/tasks?status=done
/tasks?priority=high
/tasks?tag=work
/tasks?search=meeting
```

Requirements:

* Filter by **status**
* Filter by **priority**
* Filter by **tag**
* Search in **title and description**

---

### 4. Validation & Error Handling

You must:

* Use **Pydantic models** for request/response validation
* Handle errors properly, including:

  * Invalid task ID
  * Missing required fields
  * Invalid field values

Return meaningful HTTP responses and status codes.

---

### 5. Testing

You must write tests using:

* `pytest`
* FastAPI `TestClient`

Minimum required tests:

* Creating a task
* Retrieving tasks
* Handling invalid input

---

### 6. Frontend (Static UI / Templates)

Create a simple UI using:

* Jinja2 templates OR
* Static HTML + JavaScript (fetch API)

Your UI must include:

* A page to list all tasks
* A form to create a new task

(Optional: update/delete via UI)

---

### 7. (Bonus) AI-Powered Task Suggestion 🤖

Add an endpoint:

```
POST /tasks/suggest
```

Input:

```json
{
  "text": "Prepare for backend exam"
}
```

Output:

```json
{
  "suggestions": [
    "Study APIs",
    "Practice FastAPI",
    "Revise HTTP concepts"
  ]
}
```

You can:

* Use an AI API (e.g., OpenAI), OR
* Implement a simple rule-based mock

---

## 📁 Project Structure (Suggested)

```
project/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   └── templates/
│
├── tests/
│   └── test_tasks.py
│
├── static/
│
├── requirements.txt
└── README.md
```

---

## 🧪 Evaluation Criteria

Your project will be evaluated based on:

* ✅ Correct implementation of API endpoints
* ✅ Clean and maintainable code structure
* ✅ Proper validation and error handling
* ✅ Functionality of filtering and search
* ✅ Quality of tests
* ✅ Working frontend interface
* ⭐ Bonus: AI feature

---

## 📦 Submission Guidelines

* Push your code to a **GitHub repository**
* Include a clear **README.md** with:

  * Setup instructions
  * How to run the project
  * API documentation (basic)

---

## ⚠️ Rules

* Do NOT use a database
* Do NOT copy code from others
* Keep your code clean and well-structured
* Commit regularly with meaningful messages

---

## 💡 Tips

* Start simple → then improve
* Test your API using:

  * Swagger UI (`/docs`)
  * Postman / curl
* Focus on **clarity over complexity**

---

Good luck and build something awesome 🚀

# Patient Management API

A FastAPI-based REST API for managing patient records.

## Features

* Create Patient
* View Patient
* Update Patient
* Sort Patients by Height, Weight, and BMI
* Automatic BMI Calculation
* Automatic Health Verdict Generation
* Data Validation using Pydantic

## Technologies Used

* Python
* FastAPI
* Pydantic
* JSON

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn main:app --reload
```

Open API documentation:

```text
http://127.0.0.1:8000/docs
```

# DevOps Capstone Project

[![Build Status](https://github.com/atharvgaikwad03/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/atharvgaikwad03/devops-capstone-project/actions/workflows/ci-build.yaml)

## Account Management Microservice

This project implements a RESTful microservice for managing bank accounts using Python, Flask, and PostgreSQL. It demonstrates DevOps practices including CI/CD pipelines, containerization with Docker, deployment to Kubernetes, and security implementation.

## Features

- Create, Read, Update, Delete, and List bank accounts
- RESTful API with proper HTTP status codes
- Automated CI/CD with GitHub Actions
- Containerized with Docker
- Deployed on Kubernetes (OpenShift)
- Security headers via Talisman
- CORS policies implemented

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: PostgreSQL
- **CI/CD**: GitHub Actions, Tekton
- **Container**: Docker
- **Orchestration**: Kubernetes / OpenShift
- **Testing**: nosetests, coverage
- **Code Quality**: Flake8, Pylint

## Running Locally

```bash
flask run
```

## Running Tests

```bash
nosetests
```

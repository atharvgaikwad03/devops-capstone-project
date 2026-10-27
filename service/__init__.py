"""
Account Service Package

This microservice handles the lifecycle of Accounts.
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create the Flask application
app = Flask(__name__)

# Security headers using Talisman
talisman = Talisman(app)

# CORS policies
CORS(app)

# Import routes after app is created
from service import routes, models  # noqa: F401, E402

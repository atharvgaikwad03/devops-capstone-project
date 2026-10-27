"""
Account Service Package

This microservice handles the lifecycle of Accounts.
"""
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS

# Create the Flask application
app = Flask(__name__)

# Security: Content Security Policy
talisman = Talisman(
    app,
    force_https=False,
    force_https_permanent=False,
    content_security_policy={
        'default-src': '\'self\''
    }
)

# CORS: Allow all origins
CORS(app)

from service import routes, models  # noqa: F401, E402

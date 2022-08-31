"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template, make_response

# Local modules
import config


# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("api.yml")

if __name__ == "__main__":
    connex_app.run(debug=True, port=8181)

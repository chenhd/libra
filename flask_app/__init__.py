from flask import Flask

# Initialize the app
app = Flask(
    __name__, 
    instance_relative_config=True,
    static_url_path="",
    static_folder="static",
    template_folder="templates"
    )

# Load the views
from flask_app import views

# Load the config file
app.config.from_object('config')
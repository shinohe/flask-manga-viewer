import os
from flask import Blueprint
currentDir = os.path.dirname(os.path.abspath(__file__))
app = Blueprint("dist", __name__,
    static_url_path='/sitemap', static_folder=currentDir+os.sep+'..'+os.sep+'sitemap'
)
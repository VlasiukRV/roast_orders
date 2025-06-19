import logging
import hashlib
import os
from datetime import datetime
from jinja2 import Template, Environment, FileSystemLoader

# Logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_version(file_path: str) -> str:
    with open(os.getcwd() + file_path, "rb") as f:
        file_content = f.read()
    return hashlib.md5(file_content).hexdigest()[:8]

def generate_order_id(order_time: datetime):
    timestamp = order_time.strftime("%Y%m%d%H%M%S")
    return f"ORDER_{timestamp}"

def get_template(template_name: str) -> Template:
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../templates"))

    print(f"Looking for template in: {template_dir}")
    if not os.path.exists(template_dir):
        raise FileNotFoundError(f"Template directory not found: {template_dir}")
    if template_name not in os.listdir(template_dir):
        raise FileNotFoundError(
            f"Template '{template_name}' not found in {template_dir}. Files found: {os.listdir(template_dir)}")

    env = Environment(loader=FileSystemLoader(template_dir))
    return env.get_template(template_name)
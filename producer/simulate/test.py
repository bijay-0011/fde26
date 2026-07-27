from dotenv import load_dotenv
load_dotenv(override=True)
from config_loader import CONFIG
print(CONFIG["database"])
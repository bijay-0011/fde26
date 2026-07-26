import os
import s3fs
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(override=True)

# ---------------------------------------------------------
# 1. Clear PostgreSQL
# ---------------------------------------------------------
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgrespassword")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres_oltp")
DB_NAME = os.getenv("POSTGRES_DB_OLTP", "oltp_db")
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

print("🧹 1. Cleaning PostgreSQL database...")
try:
    engine = create_engine(DB_URL)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS order_items CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS orders CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS customers CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS products CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS sellers CASCADE;"))
    print("   ✅ Dropped all existing PostgreSQL tables.")
except Exception as e:
    print(f"   ❌ PostgreSQL Cleanup failed: {e}")

# ---------------------------------------------------------
# 2. Clear MinIO Bronze Bucket
# ---------------------------------------------------------
print("🧹 2. Cleaning MinIO '01-bronze' bucket...")
try:
    fs = s3fs.S3FileSystem(
        key= os.getenv("MINIO_ACCESS_KEY"),
        secret= os.getenv("MINIO_SECRET_KEY"),
        client_kwargs={"endpoint_url": "http://localhost:9090"}
    )
    
    # Remove all contents of the bucket and recreate it
    if fs.exists("01-bronze"):
        fs.rm("01-bronze", recursive=True)
        print("   ✅ Removed existing Parquet files and folders in MinIO.")
    
    fs.mkdir("01-bronze")
    print("   ✅ Recreated clean '01-bronze' bucket.")

except Exception as e:
    print(f"   ❌ MinIO Cleanup failed: {e}")

print("\n✨ Environment completely reset! Ready for a fresh run.")
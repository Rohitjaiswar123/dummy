import os
import sqlite3
import json
from starlette.testclient import TestClient
from main import app, DB_NAME, init_db

# Reset database for clean test run
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
init_db()

client = TestClient(app)

print("=" * 60)
print("  CRASHCALL API - AUTOMATED TEST SUITE (PROOF OF WORK)")
print("=" * 60)

# TEST 1: Health Check
print("\n[TEST 1] GET /api/v1/health")
res1 = client.get("/api/v1/health")
print(f"Status Code: {res1.status_code}")
print(f"Response: {json.dumps(res1.json(), indent=2)}")
assert res1.status_code == 200, "Health check failed"

# TEST 2: Successful Registration
print("\n[TEST 2] POST /api/v1/auth/users/register (Valid Payload)")
payload = {
    "full_name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "phone": "+919876543210",
    "password": "SecurePassword123"
}
print(f"Request Payload:\n{json.dumps(payload, indent=2)}")
res2 = client.post("/api/v1/auth/users/register", json=payload)
print(f"Status Code: {res2.status_code} (Expected 201 Created)")
print(f"Response:\n{json.dumps(res2.json(), indent=2)}")
assert res2.status_code == 201, "Registration failed"
created_user_id = res2.json()["data"]["user_id"]

# TEST 3: Duplicate Email Prevention
print("\n[TEST 3] POST /api/v1/auth/users/register (Duplicate Email)")
dup_payload = {
    "full_name": "Rahul Sharma",
    "email": "rahul.sharma@example.com",
    "phone": "+919876543999",  # Different phone, same email
    "password": "AnotherPassword456"
}
res3 = client.post("/api/v1/auth/users/register", json=dup_payload)
print(f"Status Code: {res3.status_code} (Expected 409 Conflict)")
print(f"Response:\n{json.dumps(res3.json(), indent=2)}")
assert res3.status_code == 409, "Duplicate email check failed"

# TEST 4: Invalid Email & Weak Password Validation
print("\n[TEST 4] POST /api/v1/auth/users/register (Invalid Input)")
invalid_payload = {
    "full_name": "R",
    "email": "not-an-email",
    "phone": "123",
    "password": "123"  # too short
}
res4 = client.post("/api/v1/auth/users/register", json=invalid_payload)
print(f"Status Code: {res4.status_code} (Expected 422 Unprocessable Entity)")
print(f"Response:\n{json.dumps(res4.json(), indent=2)}")
assert res4.status_code == 422, "Input validation failed"

# TEST 5: Database Persistence & Bcrypt Password Hashing Check
print("\n[TEST 5] Database Verification (Checking SQLite directly)")
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("SELECT id, full_name, email, phone, password_hash, role, created_at FROM users WHERE id = ?", (created_user_id,))
row = cursor.fetchone()
conn.close()

if row:
    print(f"User in Database:")
    print(f"  - ID: {row[0]}")
    print(f"  - Full Name: {row[1]}")
    print(f"  - Email: {row[2]}")
    print(f"  - Phone: {row[3]}")
    print(f"  - Bcrypt Password Hash (Secure): {row[4][:25]}... (length: {len(row[4])})")
    print(f"  - Role: {row[5]}")
    print(f"  - Created At: {row[6]}")
    assert row[4].startswith("$2b$"), "Password is not properly hashed with bcrypt"
else:
    raise AssertionError("User was not found in SQLite database")

print("\n" + "=" * 60)
print("  ALL 5 TESTS PASSED SUCCESSFULLY! 100% OPERATIONAL")
print("=" * 60)

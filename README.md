# CrashCall API - User Registration (`POST /api/v1/auth/users/register`)

This API provides citizen registration with input validation, password hashing (bcrypt), and duplicate account conflict detection.

---

## 🚀 How to Run the Server

Open your terminal in this directory (`/Users/rohitjaiswar/manu/crashcall`) and run:

```bash
./venv/bin/uvicorn main:app --reload --port 8000
```

You will see:
```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🧪 Option A: Test in Postman (Direct Import)

A ready-made Postman collection has been prepared for you at `CrashCall_Postman_Collection.json`.

1. Open **Postman**.
2. Click the **Import** button in the top left.
3. Drag & drop the file:
   `CrashCall_Postman_Collection.json`
4. You will see 4 pre-configured requests under **CrashCall API - Proof of Work**:
   - **1. Health Check** (`GET http://127.0.0.1:8000/api/v1/health`)
   - **2. User Registration (Success - 201)** (`POST /api/v1/auth/users/register`)
   - **3. User Registration (Duplicate Email - 409 Conflict)**
   - **4. User Registration (Validation Error - 422)**
5. Click **Send** on request #2 to test registration!

---

## 🧪 Option B: Test in Postman Manually

If you want to configure Postman from scratch:

1. **Method:** Select `POST`
2. **URL:** `http://127.0.0.1:8000/api/v1/auth/users/register`
3. **Headers tab:**
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body tab:**
   - Select **raw** and choose **JSON** from the dropdown.
   - Paste:
   ```json
   {
     "full_name": "Rahul Sharma",
     "email": "rahul.sharma@example.com",
     "phone": "+919876543210",
     "password": "SecurePassword123"
   }
   ```
5. Click **Send**.
6. **Expected Response (`201 Created`):**
   ```json
   {
     "status": "success",
     "message": "User registered successfully",
     "data": {
       "user_id": "usr_7467e9fe1771",
       "full_name": "Rahul Sharma",
       "email": "rahul.sharma@example.com",
       "phone": "+919876543210",
       "role": "citizen",
       "created_at": "2026-11-23T13:05:08.284162+00:00"
     }
   }
   ```

---

## 🌐 Bonus: Interactive Web Documentation (Swagger)

While the server is running, open this URL in any browser:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

You will see the interactive Swagger UI where you and your client can inspect schemas and click **"Try it out"** to test directly in the browser!

## Project Setup

### Backend Setup

1. **Create a Virtual Environment**
   ```bash
   cd procurement_portal_backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Backend**
   ```bash
   flask run
   ```
   The backend will be available at [http://localhost:5000](http://localhost:5000).

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd procurement_portal
   npm install
   ```

2. **Build and Start the Frontend**
   ```bash
   npm run build
   npm start
   ```
   The frontend will be available at [http://localhost:3000](http://localhost:3000).

### Backend Database Setup

1. **Initialize the Database**
   ```bash
   flask db init
   ```

2. **Generate Migrations**
   ```bash
   flask db migrate -m "Initial migration."
   ```

3. **Apply Migrations**
   ```bash
   flask db upgrade
   ```

The database will be set up and ready to use.

### Notes
- Ensure you have Python and Node.js installed on your system.
- The `.env` file should be configured with the necessary environment variables. Make sure it is not tracked by Git as it contains sensitive information.

.env folder should be in the procurement_portal_backend and include:
FLASK_APP=run.py
FLASK_ENV=development
openai_api_key=XXXX

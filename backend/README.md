# SE-Project Backend

## Project Structure

The backend for the SE-Project is organized into the following directories:

- `chatbot`: Contains the chatbot functionality.
- `server`: Contains the Flask server code.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd soft-engg-project-jan-2025-se-Jan-21/backend
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add a `.env` file to the root directory:**
   Create a file named `.env` in the backend directory and add the following content:

   ```
   GROQ_API_KEY=<your-groq-api-key>
   ```

5. **Update `requirements.txt` when adding new packages:**
   Whenever you add a new package to the code, make sure to update the `requirements.txt` file:
   ```bash
   pip freeze > requirements.txt
   ```

## Additional Information

For more details on the chatbot functionality and server endpoints, refer to the respective directories' README files.

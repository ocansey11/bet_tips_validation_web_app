# Setting Up the Project

1. **Choose a Database**  
    Decide which database you want to use for the project. Previously, SQL was used, but this may change based on your requirements.

2. **Create a Virtual Environment**  
    Run the following command to create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**  
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install Requirements**  
    Install the required dependencies using:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Application**  
    Navigate to the `app` directory and start the Flask application:
    ```bash
    cd app
    flask run
    ```

6. **Database Flexibility**  
    You can switch to a different database as long as you are familiar with its configuration and integration with the application. Currently, there are plans to transition to MongoDB.

7. **AI Integration**  
    The application will include AI agents to enhance its capabilities, leveraging transfer learning for improved predictions and decision-making.

8. **Project Status**  
    This application is undergoing reconstruction, with plans to incorporate MongoDB and AI-driven features for enhanced functionality.


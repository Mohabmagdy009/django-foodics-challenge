# Backend Challenge Solution

## Overview

This project is a solution to the backend challenge, which includes an inventory system for managing products and ingredients. It supports order creation, stock management, email notifications for low stock levels, and includes a Swagger API for easy interaction with the endpoints.

The project includes the following features:
- Product and ingredient management
- Order creation and stock update
- Email notifications triggered when stock levels fall below a defined threshold
- A Swagger UI for easy access to the API

## ERD

An Entity-Relationship Diagram (ERD) illustrating the structure of the database is included as `erd.jpeg` in the project. It provides a visual representation of the relationships between the models.

## Swagger UI

The API documentation is available via the Swagger UI. You can access it by visiting the following endpoint after running the project:


This provides a fully interactive interface to test and explore the available endpoints.

## Getting Started

You have two options for starting the project:

### Option 1: Manually

1. **Create the `.env` file**:
   - Copy the contents of `.env.example` into a new file named `.env`.

2. **Create a virtual environment**:
   - Run the following command to create a virtual environment named `.venv`:
     ```bash
     python -m venv .venv
     ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install the dependencies**:
   - Navigate to the backend directory:
     ```bash
     cd backend
     ```
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the database migrations**:
   ```bash
   python manage.py migrate

6. **Create the system user**:
   ```bash
    python manage.py create_system_user
   
7. **Seed the database**:
   ```bash
    python manage.py loaddata ingredients.json product_ingredients.json products.json

8. **Start the development server**:
   ```bash
    python manage.py runserver

### Option 2: Automatically
1. **Run the run_it_for_me.sh script**:
   - First, visit the run_it_for_me.sh file and uncomment the appropriate command based on your 
   operating system (macOS/Linux or Windows).
2. **Execute the script using sh command**

## Project Structure
1. **backend/**: Contains the main project code, including models, views, and serializers.
2. **erd.jpeg**: Entity-Relationship Diagram for the database.
3. **.env.example**: Example environment file for setting up configuration.
4. **run_it_for_me.sh**: Shell script to automate the setup process.
5. **requirements.txt**: The list of Python dependencies required for the project.

## Testing
### Unit Tests
**The project includes a set of unit tests to verify the functionality of the system. 
You can run the tests using the following command**:

```bash
python manage.py test
```

### Manual Testing
- Use the Swagger UI to test the API endpoints interactively.
- Make sure the email notification logic works by simulating 
low stock levels through order creation.

### Conclusion
- This project implements the required functionality for managing an inventory system 
with stock and order management, email notifications, and an API interface. 
You can access the API via Swagger, and the project setup is straightforward with both manual and automated options available.
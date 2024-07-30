# ToDo List Web Application

## Project Requirements
This project is a web application for managing to-do lists. The main features include:

- **Personal and Shared Lists**: Users can view only their personal lists but have the ability to share lists with others.
- **User Authentication**: Includes login, signup with email verification, and single sign-on functionality.
- **Task Management**: Users can create, delete, and manage tasks with due dates, descriptions, titles, and creation dates.
- **Email Notifications**: Users receive email reminders for tasks due soon.
- **CAPTCHA**: Ensures valid task creation through CAPTCHA verification.
- **Social Sharing**: Tasks can be shared on social media platforms such as Facebook, LinkedIn, and Twitter.

## Features

### User Authentication
- **Signup**: Users can sign up with their email, username, and password. An email with an activation link is sent for account verification.
- **Login**: Users can log in with their credentials. Option to remember the user or expire the session on browser close.
- **Logout**: Users can log out of their accounts.

### Task Management
- **Create Task**: Users can create tasks with a title, description, and due date. CAPTCHA verification ensures valid submissions.
- **Delete Task**: Users can delete their tasks.
- **Share Task**: Users can share tasks with others through unique tokens. Shared tasks can be copied to the recipient's list.

### Email Notifications
- **Due Date Reminder**: An email reminder is sent to users a day before the task's due date.

## Code Structure

### `views.py`
Handles the main functionality of the application, including user authentication, task management, and email notifications.

### `tokens.py`
Defines a custom token generator for account activation.

### `scheluder.py`
Sets up a scheduler to send email reminders for tasks due the next day.

### `models.py`
Defines the database models for `Note` and `SharedNote`.

### `admin.py`
Registers the models with the Django admin site for easy management.

## Getting Started

### Prerequisites
- Python 3.x
- Django
- Django-APScheduler
- Django-ReCaptcha

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Has-sh/ToDoListApp.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ToDoListApp/Intern_project_app
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the migrations:
    ```bash
    python manage.py migrate
    ```
5. Start the development server:
    ```bash
    python manage.py runserver
    ```

### Configuration
1. Set up the email backend in `settings.py` for sending email notifications.
2. Configure ReCaptcha keys in `settings.py`.

## Usage
1. Navigate to the signup page and create a new account.
2. Log in to your account.
3. Create, delete, and share tasks.
4. Receive email reminders for tasks due soon.

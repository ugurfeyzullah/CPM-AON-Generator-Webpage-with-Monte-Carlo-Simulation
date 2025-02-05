# CPM (AON) Generator – Project Management Assistant

![image](https://github.com/user-attachments/assets/e599349e-eddc-4a90-a864-8345a5cc79e6)
![image](https://github.com/user-attachments/assets/4ef5f0c4-ca21-466b-94b3-daff757b0c4c)



## Table of Contents
- [Abstract](#abstract)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Abstract

This web application is a comprehensive project management assistant built with Flask. It allows users to:
- Generate Activity Network Diagrams (CPM/AON) from manual inputs or Excel file uploads.
- Perform Monte Carlo simulations to analyze project scheduling uncertainties.
- Visualize network diagrams, Gantt charts, S-curves, and criticality index charts.
- Interact with a Chat Bot (powered by OpenAI) that helps format and interpret project data.
- Manage user accounts (signup, login, logout) and submit feedback.

The system integrates various tools (Flask, SQLAlchemy, Graphviz, Matplotlib, and OpenAI) to support project planning, scheduling, and analysis.


https://github.com/user-attachments/assets/e47dc8c4-310a-48ac-aff0-e999a2cb31e9


## Features

- **Excel Import:**  
  Upload Excel files with activities, durations, and successors to generate network diagrams.
- **CPM Analysis:**  
  Compute earliest start/finish and latest start/finish times to identify critical paths.
- **Monte Carlo Simulation:**  
  Run simulations to estimate project completion times and assess uncertainties.
- **Graph Generation:**  
  Generate network diagrams using Graphviz and Gantt charts using Matplotlib.
- **Chat Bot Interface:**  
  Interact with an OpenAI-powered Chat Bot for project management guidance.
- **User Authentication:**  
  Signup, login, and logout using Flask-SQLAlchemy and secure password hashing.
- **Feedback Submission:**  
  Users can submit feedback that is stored in a SQLite database.
- **Email Notifications:**  
  Send welcome emails upon signup using Flask-Mail.

## Installation

### Prerequisites

- **Python 3.9** (or later)
- **Flask** (and related packages listed in `requirements.txt`)
- A web browser to access the application

**Additional Software Requirements:**

- **Graphviz:** Make sure Graphviz is installed on your system (for generating network diagrams).  
- **SMTP Email Account:** (e.g., Outlook, Gmail) for sending emails via Flask-Mail.  
- **SQLite:** (Installed by default with Python) for the database backend.

### Steps

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```
2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up Environment Variables:**  
   Create a `.env` file (or set system environment variables) for sensitive information. For example:
    ```
    SECRET_KEY=your_secret_key
    MAIL_USERNAME=your_email@example.com
    MAIL_PASSWORD=your_email_password
    OPENAI_API_KEY=your_openai_api_key
    SQLALCHEMY_DATABASE_URI=sqlite:///users.db
    ```
4. **Run the Application:**
    ```bash
    flask run
    ```
   The application will be available at `http://localhost:5000/`.

## Usage

- **Home Page (Activity Network Diagram):**  
  Manually input project activities, durations, and successors or import data from an Excel file.  
  The system will generate a network diagram, calculate critical path metrics, and display a Gantt chart.

- **Monte Carlo Simulation:**  
  Navigate to the simulation tab to run project schedule simulations. View simulation results, including S-curves and criticality index charts.

- **Chat Bot:**  
  Use the Chat Bot interface to ask questions about project management or request help with formatting activity data.  
  The Chat Bot processes your input (via OpenAI's GPT model) and returns formatted project data.

- **User Authentication:**  
  Sign up, log in, and log out using the provided forms.  
  Once logged in, users can also delete their account.

- **Feedback:**  
  Submit feedback via the feedback form. Your comments are stored in the database and can be viewed by administrators.


## Contributing

Contributions are welcome! If you have improvements or bug fixes, please follow these steps:

1. Fork the repository.
2. Create your feature branch:
    ```bash
    git checkout -b feature/YourFeature
    ```
3. Commit your changes:
    ```bash
    git commit -am 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/YourFeature
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Contact

- **Feyzullah Yavan**  
  Email: [feyzullah.yavan@kit.edu](mailto:feyzullah.yavan@kit.edu)  
  LinkedIn: [https://www.linkedin.com/in/ugurfey](https://www.linkedin.com/in/ugurfey)


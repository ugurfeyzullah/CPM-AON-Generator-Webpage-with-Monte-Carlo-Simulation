Project Management Tool with Flask
This repository contains a Flask web application designed to facilitate project management through the implementation of Critical Path Method (CPM) and Monte Carlo simulations. It allows users to upload project data via Excel files, automatically generates CPM diagrams and Gantt charts, and performs simulations to predict project duration.

Features
Excel File Upload: Users can upload project data through Excel files, specifying activities, durations, dependencies, and more.
Critical Path Method (CPM): The tool calculates and visualizes the critical path, earliest start and finish, latest start and finish, and slack times for project activities.
Gantt Chart Generation: Automatically generates Gantt charts for visualizing project timelines.
Monte Carlo Simulations: Performs Monte Carlo simulations to analyze the variability in project duration, taking into account uncertainties in activity durations.
Getting Started
Prerequisites
Python 3.6 or higher
Flask
Pandas
NumPy
Matplotlib
Graphviz

Usage
Start the application
Access the web interface: Open your browser and navigate to http://127.0.0.1:5000/.
Upload an Excel file: Use the upload feature to submit your project data in the specified format.
View the CPM and Gantt chart: The application will process the data and display the critical path and Gantt chart.
Perform simulations: Navigate to the simulations tab to perform Monte Carlo simulations and analyze the project duration variability.

Contributing
Contributions to this project are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.

Contact
Feyzullah Yavan - www.linkedin.com/in/ugurfey - uguryavan@hotmail.com


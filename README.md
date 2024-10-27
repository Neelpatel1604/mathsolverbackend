#  Math Solver Backend
This repository contains the backend implementation of the Math Solver application, which handles various mathematical operations and provides APIs to interact with the frontend.

## Getting Started
Prerequisites
Make sure you have Python installed on your system. It's recommended to use a virtual environment to manage dependencies.

## Setup
Clone the repository:

```bash

git clone <repository-url>
```
```bash
Navigate to the project directory:
cd <project-directory>
```
Activate the virtual environment:
On Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```
Install the required packages:
```bash
pip install -r requirements.txt
```
Running the Backend
To run the backend server, use the following command:
```bash
python app.py
```
The server will start, and you can access the backend services through the exposed endpoints.

## Connecting to the Frontend
The frontend part of this application is hosted in a separate repository. To run the complete application, follow the setup instructions provided in the [mathsolverfrontend](). Make sure the backend is running before starting the frontend.

## Project Structure
- app.py: The main backend script to run the server.
- cardano_method.py: Implements Cardano's method for solving polymial equations.
- matrix_operations.py: Contains various matrix operations.
- test_solvers.py: Test scripts for validating mathematical solvers.
- venv/: Virtual environment directory.
- node_modules/: Contains Node.js modules (used if frontend is linked).
- pyproject.toml: Python project configurations.
- package.json: Node.js package configuration.
  
## Contributions
Feel free to fork this repository and submit pull requests for improvements. Make sure to follow best practices and write tests for new features.

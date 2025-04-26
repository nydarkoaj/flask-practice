# Flask Practice

This project is a practice repository for learning and experimenting with Flask.

## Features

- Basic Flask application setup
- Example routes and templates
- Integration with a 'database' - jsonified list of dicts for simplicity

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nydarkoaj/flask-practice.git
   ```
2. Navigate to the project directory:
   ```bash
   cd flask_practice
   ```
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set environment variables
   ```bash
   export FLASK_APP=flash.py
   export FLASK_ENV=development 
   ```

## Usage

1. Run the Flask application in debug mode:
   ```bash
   flask run --debug
   ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features.

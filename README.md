# LyricsMatch

🎵 A fun game to match song lyrics with their titles! This project consists of a backend built with Python (Flask) and a frontend built with React.

## Description

LyricsMatch is a web application that generates random song lyrics and challenges users to guess the correct song title. The application provides immediate feedback on whether the guess is correct or not.

## Project Structure

- `app.py`: Contains the backend code, which is built using Flask.
- `frontend/`: Contains the frontend code, which is built using React.

## Features

- Generate random song lyrics snippets
- Input field to guess the song title
- Immediate feedback on the correctness of the guess

## Installation

### Backend

1. **Clone the repository:**

    ```bash
    git clone https://github.com/shwetajha977/LyricsMatch.git
    cd LyricsMatch
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the backend server:**

    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run
    ```

    The backend will be available at `http://127.0.0.1:5000`.

### Frontend

1. **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2. **Install the required dependencies:**

    ```bash
    npm install
    ```

3. **Start the development server:**

    ```bash
    npm start
    ```

    The frontend will be available at `http://localhost:3000`.

## Usage

1. Open the application in your browser.
2. Click on the "Generate Lyric Snippet" button to fetch a random lyric.
3. Enter your guess for the song title in the input field.
4. Click "Check Answer" to see if your guess is correct.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch with a descriptive name.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or issues, please contact [shwetajha977](https://github.com/shwetajha977).

---

This README file provides a basic overview of the project, its installation, usage, and contribution guidelines. Feel free to customize it further to fit your project's needs.

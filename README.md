# Vote API v1

## Overview
The Vote App is a simple real-time voting application developed using Python, FastAPI, and SQLModel. This application allows users to cast votes, which are stored in a SQLite database, and observe real-time vote counts via a WebSocket connection.

## Features
- Real-time vote count updates through WebSocket.
- RESTful API endpoints to cast votes and retrieve vote data.
- SQLite database to store vote data.

## Getting Started

### Prerequisites
- Python 3.8 or later.
- FastAPI
- SQLModel
- SQLite

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/vote-app.git
   cd vote-app
   ```
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn sqlmodel
   ```
4. Create the initial database and tables:
   ```bash
   python config/database.py
   ```

### Running the App
1. Start the FastAPI server:
   ```bash
   uvicorn main:vote_app --host 0.0.0.0 --port 9000 --reload
   ```
2. Open your browser and navigate to [http://127.0.0.1:9000/docs](http://127.0.0.1:9000/docs) to access the FastAPI Swagger UI, where you can interact with the API endpoints.

### WebSocket Client
Connect a WebSocket client to `ws://127.0.0.1:9000/v1/ws/` to receive real-time vote count updates.

### API Endpoints
- **POST** `/v1/vote/`: Cast a new vote.
- **GET** `/v1/vote/`: Retrieve all votes from the database.

## Contributing
To contribute to this project, create a new branch, make your changes, and submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact
For any inquiries, feel free to open an issue or contact the repository owner.

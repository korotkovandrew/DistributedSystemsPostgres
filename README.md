# University Database Management System

This project demonstrates a distributed database system with PostgreSQL replication and a Flask-based server. It includes a client application with a Tkinter GUI for managing student records.

- **PostgreSQL Primary and Replica**: Two PostgreSQL containers with streaming replication.
- **Flask Server**: Handles CRUD operations for the `students` table.
- **Tkinter Client**: A GUI application for interacting with the server.

The project includes sample data for testing.

## Prerequisites

- **Git**: Ensure Git is installed on your system.
- **Docker**: Ensure Docker and Docker Compose are installed and running.

## Getting Started

Follow these steps to set up and run the project:

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/korotkovandrew/DistributedSystemsPostgres
cd DistributedSystemsPostgres
```
### 2 Start the Containers
```
docker compose up -d --build
```

### 3 Install Client Dependencies
The client (client.py) requires Python and the requests library. Install the dependencies:
```
pip install -r requirements_manual.txt
```

### 4 Run the Client
Launch the Tkinter GUI client:
```
python ./client/client.py
```

### (5) Stoppping the Application
To stop and remove the containers:
```
docker compose down -v
```
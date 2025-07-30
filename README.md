## I-Stem Task GenAI Voice Pipeline Agent

This repository contains the code for the I-Stem Task GenAI Voice Pipeline Agent, which is designed to facilitate voice-based interactions uisng LiveKit.

### Folder Structure

- `config/`: Contains configuration files, environment variables. (Put your `.env` file here)
- `services/`: Contains service classes that handle various functionalities. (Currently has just `chart_handler`)
- `task<number>/`: Contains task-specific implementations.


### Usage
1. Clone the repository.
2. Install the required dependencies using `uv sync`.
3. Set up your environment variables in the `.env` file using `.env.example` in the `config/` directory.
4. Run each task using the command `uv run -m task<number>.<file_name> console`.
5. For example, to run the first task, use `uv run -m task1.baseline console`.
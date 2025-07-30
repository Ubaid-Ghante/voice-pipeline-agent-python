## I-Stem Task GenAI Voice Pipeline Agent

This repository contains the code for the I-Stem Task GenAI Voice Pipeline Agent, which is designed to facilitate voice-based interactions uisng LiveKit.

### Folder Structure

- `config/`: Contains configuration files, environment variables. (Put your `.env` file here)
- `services/`: Contains service classes that handle various functionalities. (Currently has just `chart_handler`)
- `task<number>/`: Contains task-specific implementations.


### Usage
1. Clone the repository.
2. Install the required dependencies using 
```bash
uv sync
```
3. Set up your environment variables in the `.env` file using `.env.example` in the `config/` directory.
4. Run each task using the command 
```bash
uv run -m task<number>.<file_name> console
```
5. For example, to run the first task, use 
```bash
uv run -m task1.baseline console
```

## Complete Explanation and Demo

For a complete explanation of the task see the presentation [here](https://www.canva.com/design/DAGukVDdZqw/YY_gFNCEjTEAVpnIBXPbAw/edit?utm_content=DAGukVDdZqw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

OR you can go through this pdf
[<img src="./static/Task I-Stem.jpg">](./static/Task%20I-Stem.pdf)

##### Demo Video
[<video src='./static/Screen Recording 2025-07-30 at 12.45.10 PM.mov' width=480/>](./static/Screen%20Recording%202025-07-30%20at%2012.45.10%C2%A0PM.mov)
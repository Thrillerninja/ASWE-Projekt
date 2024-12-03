# ASWE-Projekt
## Dependencies

### PyQt5
### PyQt5

To use PyQt5 on Windows, you need to install Microsoft Build Tools for C++.
To use PyQt5 on Windows, you need to install Microsoft Build Tools for C++.

1. Download and install Microsoft Build Tools for C++ from the [official website](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. During installation, select the **"Desktop development with C++"** workload to include the necessary components.

This step is essential for building certain components of PyQt5.

### Ollama

This software utilizes AI through the free tool Ollama. The easiest way to run Ollama is in a container.

1. Ensure you have Docker installed.
2. Run Ollama as a container with the following command (the port is important):
    ```bash
    docker run -d --name ollama -p 11434:11434 -v ollama_storage:/root/.ollama ollama/ollama:latest
    ```
3. Enter the Ollama Docker container shell and pull the specified model (default is llama3.2:1b):
    ```bash
    ollama pull llama3.2:1b
    ```
4. Ollama should now be running in a container with llama3.2 installed and ready to use.

### Python Dependencies

To install the necessary Python packages, follow these steps:

1. Open a terminal and navigate to the root directory of the project:
    ```bash
    cd YOUR_PATH/ASWE-Projekt
    ```
2. Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
3. All necessary packages should now be installed.


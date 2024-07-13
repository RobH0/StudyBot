# StudyBot

A note taking assistant that can help you summarize educational YouTube videos into concise study notes.

## Installation

### Setup Ollama server
1. Download Ollama from [ollama.com/download](https://ollama.com/download) following the installation instructions provided by Ollama's website.
2. Once ollama is installed, open terminal or command prompt and pull the gemma2:9b model:
    ```
    ollama pull gemma2:9b
    ```
3. Start the local ollama server:
    ```
    ollama serve
    ```

### Setup StudyBot environment and install dependancies
1.  Clone the repository:
    ```
    git clone https://github.com/RobH0/StudyBot.git
    ```
2. Create Python3 virtual environment and activate it:
    ```
    # Linux create venv
    python3 -m venv env
    # Linux activate venv
    source env/bin/activate

    # Windows create venv
    python -m venv env
    # Windows activate venv
    venv\Scripts\activate
    ```
3. Install python3 dependancies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Make sure Ollama server is running:
    ```
    ollama serve
    ```
2. Execute the study_bot.py script:
    ```
    # Linux
    python3 study_bot.py
    
    # Windows
    python study_bot.py
3. Respond to prompts displayed in your terminal.

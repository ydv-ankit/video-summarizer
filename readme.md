## Video Summarizer

- upload video in any language and get its summary in english within seconds

## How it works

- upload video
- extract audio
- convert audio to text (STT)
- process extracted text with LLM and summarize
- serve the summarized text to client

## Want to run locally?

### (With Docker)

0. **_make sure you have `docker` installed and running on your machine_**

1. Clone the repo

   ```bash
   git clone https://github.com/ydv-ankit/ai-video-summarizer.git
   ```

2. start docker containers using docker compose file: `docker.compose.yml`, present in the cloned directory

   ```bash
   docker compose -f ./docker.compose.yml up -d
   ```

3. your server is running on localhost: [http://localhost:8000](http://localhost:8000)

### (Without Docker)

0. **_Make sure you have installed `python >= 3.10`_**
1. Clone the repo

   ```bash
   git clone https://github.com/ydv-ankit/ai-video-summarizer.git
   ```

2. Change current working directory

   ```bash
   cd ai-video-summarizer
   ```

3. create a virtual environment

   ```bash
   python3 -m venv myenv
   ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

5. Start fastapi server in development mode

   ```bash
   fastapi dev main.py
   ```

6. Server is up and running on localhost: [http://localhost:8000](http://localhost:8000)

### Feel free to suggest changes.

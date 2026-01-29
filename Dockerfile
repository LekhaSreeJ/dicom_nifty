# 1. Base Image - Python light version
FROM python:3.9-slim

# 2. Project folder-ah docker kulla create pandrom
WORKDIR /app

# 3. Necessary tools install pandrom
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Requirements-ah copy panni install pandrom
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Full project code-ah copy pandrom
COPY . .

# 6. Streamlit port-ah expose pandrom
EXPOSE 8501

# 7. Healthcheck (Optional but good for 35+ LPA standards)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 8. App-ah run panna command
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Step 1: Base image
FROM python:3.9-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Install system dependencies (Medical imaging libraries-ku idhu thevai)
# OpenCV and SimpleITK-ku sila basic libraries keta kooda idhu handle pannidum
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy requirements first (Optimization trick!)
COPY requirements.txt .

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the code
COPY . .

# Step 7: Port exposure
EXPOSE 8501

# Step 8: Command
CMD ["streamlit", "run", "main_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Use Python 3.12 base image
FROM python:3.12-slim

# Install dependencies
RUN apt update && apt install -y wget unzip curl \
    && wget -q -O /usr/bin/google-chrome https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && wget -q -O chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver.zip -d /usr/local/bin/ \
    && rm chromedriver.zip

# Set environment variables
ENV PATH="/usr/local/bin:${PATH}"

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]

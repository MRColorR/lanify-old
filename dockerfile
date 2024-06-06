FROM debian:stable-slim

# Set environment variables
ENV EXTENSION_ID=fljkmocmlejbiaohjiecblmdjpaohapdom
ENV EXTENSION_URL='https://app.lanify.ai/'

# Install necessary packages then clean up to reduce image size
RUN apt update && \
    apt upgrade -y && \
    apt install -qqy \
    curl \
    wget \
    git \
    chromium \
    chromium-driver \
    python3 \
    python3-selenium && \
    apt autoremove --purge -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Download crx downloader from git
RUN git clone "https://github.com/warren-bank/chrome-extension-downloader.git" && \
    chmod +x ./chrome-extension-downloader/bin/*

# Download the extension selected
RUN ./chrome-extension-downloader/bin/crxdl $EXTENSION_ID

# Install python requirements
RUN pip install -r requirements.txt 
COPY main.py .

ENTRYPOINT [ "python3", "main.py" ]

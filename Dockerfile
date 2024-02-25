FROM rasa/rasa:2.8.0 

# Set environment variables
ENV PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_TIMEOUT=600

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set permissions for the site-packages directory
RUN chmod -R a+w /opt/venv/lib/python3.10/site-packages/

EXPOSE 5005

CMD ["run", "-m", "/app/models", "--enable-api", "--cors", "*"]

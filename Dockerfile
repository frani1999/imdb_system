# docker/Dockerfile

FROM python:3.10-slim

# Work directory
WORKDIR /app

# Add PYTHONPATH to WORKDIR
ENV PYTHONPATH=/app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY system_module_1/ ./system_module_1/
COPY system_module_2/ ./system_module_2/

# Port exposed
EXPOSE 8000
EXPOSE 5432

# Start server
CMD ["uvicorn", "system_module_2.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.12-slim

WORKDIR /app

# Install UV for better dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies using UV
RUN uv pip install --system .

# Copy service code
COPY . .

# Expose port
EXPOSE 8000

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
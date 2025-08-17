FROM python:3.11

WORKDIR /app

# Install build tools
RUN pip install --upgrade pip setuptools wheel build

# Copy metadata and actual code before install
COPY pyproject.toml README.md ./
COPY expedia_travel_recommendations ./expedia_travel_recommendations

# Install the package via pyproject.toml
RUN pip install .

# Expose MCP port
EXPOSE 9900

# Use installed package (module-style) if it works, or fallback to file path
ENTRYPOINT ["fastmcp", "run", "expedia_travel_recommendations/main.py", "--transport", "streamable-http", "--port", "9900", "--host", "0.0.0.0"]
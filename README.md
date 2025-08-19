# 🌍 Expedia Travel Recommendations MCP Server

This project provides an **MCP (Model Context Protocol)** server that exposes Expedia Travel Recommendations (hotels, flights, activities, and cars) via both **stdio** and **streamable-http** protocols—ideal for LLM integrations and web-based applications.

---

## ✨ Features

- 🔌 MCP server integration for Expedia's travel recommendation APIs  
- 📦 Supports both `stdio` and `streamable-http` protocols  
- 🏨 Hotel, ✈️ Flight, 🗺️ Activity, and 🚗 Car rental recommendations  
- 🔐 API key-based secure access  

---

## 🛠 Prerequisites

- Python **3.11+**
- Expedia **API key**

---

## 🚀 Installation

### 1️⃣ Clone and Build the Python Package

```bash
git clone <repository-url>
cd expedia-travel-recommendations-mcp
chmod +x build.sh
./build.sh
```

> This will build the Python wheel and output it under the `dist/` directory.

---

### 2️⃣ Install in a Virtual Environment

```bash
chmod +x install.sh
./install.sh
```

> Creates a virtual environment, installs the built wheel into it.

---

## ⚡ Running the MCP Server

### Run with `stdio` protocol (LLM Integration)

```bash
chmod +x run.sh
./run.sh "your_api_key" "stdio"
```

### Run with `streamable-http` protocol (Web Clients)

```bash
./run.sh "your_api_key" "streamable-http"
```

> Access it at: `http://0.0.0.0:9900/mcp`

---

## 🐳 Running with Docker

### Using Docker Compose (Recommended)

```bash
chmod +x docker_run.sh
./docker_run.sh
```

> Accessible at: `http://0.0.0.0:9900/mcp`

---

## ⚙️ MCP Client Configuration

```json
{
  "mcpServers": {
    "expedia-recommendation": {
      "url": "http://localhost:9900/mcp"
    }
  }
}
```

---

## 🧪 Example Query (Hotel)

```json
{
  "query": {
    "destination": "Seattle",
    "check_in": "2025-05-01",
    "check_out": "2025-05-05",
    "property_types": ["HOTEL", "RESORT"],
    "amenities": ["POOL", "SPA"],
    "guest_rating": "WONDERFUL",
    "sort_type": "CHEAPEST"
  }
}
```

---

## 🔗 API Endpoints

> These are exposed when using the `streamable-http` protocol.

- `POST /expedia/hotels` → Hotel recommendations  
- `POST /expedia/flights` → Flight recommendations  
- `POST /expedia/activities` → Activity recommendations  
- `POST /expedia/cars` → Car rental recommendations  

---

## 🧑‍💻 Example Clients

See the `examples/` folder for client scripts.

### 1️⃣ stdio-based Client

Make sure the virtual env is activated (`install.sh` must be run first):

```bash
source install_env/bin/activate
python examples/mcp_client_stdio.py
```

### 2️⃣ streamable-http Client

Ensure MCP server is running:

```bash
python examples/mcp_client_streamable_http.py
```

---

## 📄 License

Licensed under the [Apache License 2.0](LICENSE).

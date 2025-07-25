# OCR Receipt Total Extractor

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A **FastAPI**-based web application that uses OCR (Optical Character Recognition) to automatically extract totals from receipt and invoice images. The system is containerized with Docker for simple and fast deployment.

## ✨ Features

- **🔍 Intelligent OCR**: Smart total extraction from receipt images using advanced pattern recognition
- **📸 Multi-format Support**: Supports all common image formats (JPEG, PNG, WEBP, BMP, TIFF)
- **🌐 Web Interface**: easy image uploads
- **🚀 REST API**: RESTful endpoints for programmatic integrations
- **🌍 Multi-language**: Recognizes totals in Italian, English, French, German, and Spanish
- **💾 Data Persistence**: Automatic saving of results in JSON format
- **🐳 Containerized**: Docker and Docker Compose

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed on your system
- At least **2GB of RAM** available (for OCR models)
- **Port 8000** available
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### Method 1: Docker Compose (Recommended)

1. **Clone the repository**:
   git clone <repository-url>
   cd ocr-receipt-extractor

### 2. **Avvio applicativo Docker**

- **docker compose up -d**
- **docker compose ps**

### Metodo 2: Local Installation

- **pip install -r requirements.txt**
- **uvicorn main:app --host 0.0.0.0 --port 8000**

### **PROJECT STRUCTURE**

ocr-receipt-extractor/
├── main.py                 
├── requirements.txt        
├── Dockerfile            
├── docker-compose.yml     
├── templates/
│   └── index.html         
├── static/                
├── data/
│   ├── media/            
│   └── data.json         
└── README.md 
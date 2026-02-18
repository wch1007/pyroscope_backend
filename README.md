# Pyroscope Dashboard - Fire Risk Monitoring System

A comprehensive wildfire risk monitoring and prediction system using autonomous robots for environmental data collection and analysis.

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Backend)
- **Node.js 16+** (Frontend)
- **MySQL 8.0+** (Database)

### Starting the Application

#### 1. Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if using)
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

#### 2. Start Frontend Development Server

```bash
# In a new terminal, navigate to project root
cd pyroscope_dashboard

# Start Vite development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Heatmap System](#heatmap-system)
- [Data Generation](#data-generation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## ✨ Features

### Core Functionality

- **Real-time Environmental Monitoring**
  - Air temperature and humidity
  - Ground temperature measurement
  - Wind speed tracking
  - GPS-based location tracking

- **Advanced Heatmap Visualization**
  - 7 interactive heatmap layers
  - Bilinear interpolation for smooth gradients
  - Multiple fuel load indicators
  - Integrated fire risk assessment

- **Autonomous Scanning**
  - 50m × 50m scan area coverage
  - 20 × 20 measurement grid (400 points)
  - 2.5m point spacing for high resolution
  - Automated data collection

- **Fire Risk Analysis**
  - Real-time risk calculation
  - Multi-factor assessment (temperature, humidity, fuel)
  - Historical trend analysis
  - Risk level classification

### Heatmap Layers

1. **Ground Temperature** - Surface temperature distribution
2. **Air Temperature** - Atmospheric temperature patterns
3. **Air Humidity** - Moisture level mapping
4. **1-Hour Fuel** - Fast-burning vegetation
5. **10-Hour Fuel** - Medium-burning materials
6. **100-Hour Fuel** - Slow-burning large fuels
7. **Fire Risk** - Overall fire danger assessment

---

## 🛠 Technology Stack

### Frontend

- **Framework**: React 18
- **Build Tool**: Vite
- **Map Library**: Leaflet + React-Leaflet
- **UI Components**: Lucide React Icons
- **Styling**: CSS3 with CSS Variables

### Backend

- **Framework**: FastAPI (Python)
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Migration**: Alembic
- **Web Scraping**: Selenium (for fuel estimation)

### Data Processing

- **Interpolation**: Bilinear interpolation algorithm
- **Visualization**: Canvas 2D + ImageOverlay
- **Data Generation**: NumPy + sine wave algorithms

---

## 📦 Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-repo/pyroscope_dashboard.git
cd pyroscope_dashboard
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pyroscope_db
DB_USER=your_username
DB_PASSWORD=your_password

# API Configuration
API_PORT=8000
DEBUG=True

# Fuel Estimation API (optional)
FUEL_ESTIMATION_API_URL=https://www.wfas.net/nfdr-fuel-moisture/
FUEL_ESTIMATION_TIMEOUT=60
FUEL_ESTIMATION_HEADLESS=True
```

#### Setup Database

```bash
# Access MySQL
mysql -u root -p

# Create database
CREATE DATABASE pyroscope_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Run migrations
cd backend
alembic upgrade head
```

### 3. Frontend Setup

```bash
# Navigate to project root
cd pyroscope_dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📁 Project Structure

```
pyroscope_dashboard/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   │   ├── scan.py      # Scan records
│   │   │   ├── environmental.py  # Environmental data
│   │   │   └── image.py     # Image records
│   │   ├── routers/         # API endpoints
│   │   │   ├── scans.py     # Scan operations
│   │   │   └── images.py    # Image handling
│   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── scan.py
│   │   │   ├── environmental.py
│   │   │   └── heatmap.py
│   │   ├── services/        # Business logic
│   │   │   ├── scan_service.py
│   │   │   └── fire_risk_service.py
│   │   ├── database.py      # Database connection
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   ├── generate_ultra_dense_grid.py  # Data generation
│   ├── update_scan_aggregates.py     # Statistics update
│   └── requirements.txt
├── src/
│   ├── components/
│   │   ├── HeatmapPanel.jsx      # Main heatmap component
│   │   ├── SimpleHeatmap.jsx     # Interpolated heatmap
│   │   ├── ScanResults.jsx       # Detailed scan view
│   │   ├── DataLog.jsx           # Data table
│   │   ├── Sidebar.jsx           # Left sidebar
│   │   └── Map.jsx               # Main map
│   ├── services/
│   │   └── api.js                # API client
│   ├── App.jsx                   # Main application
│   └── main.jsx                  # Entry point
├── public/                  # Static assets
├── package.json
└── vite.config.js
```

---

## ⚙️ Configuration

### Database Schema

#### `scan_records` Table

```sql
CREATE TABLE scan_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id VARCHAR(50) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    avg_plant_temp DECIMAL(5, 2),
    avg_air_temp DECIMAL(5, 2),
    avg_humidity DECIMAL(5, 2),
    fuel_load DECIMAL(10, 4),
    risk_level VARCHAR(20),
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### `environmental_data` Table

```sql
CREATE TABLE environmental_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scan_id INT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    air_temperature DECIMAL(5, 2),
    air_humidity DECIMAL(5, 2),
    plant_temperature DECIMAL(5, 2),
    one_hour_fuel DECIMAL(10, 4),
    ten_hour_fuel DECIMAL(10, 4),
    hundred_hour_fuel DECIMAL(10, 4),
    measured_at DATETIME,
    FOREIGN KEY (scan_id) REFERENCES scan_records(id)
);
```

---

## 🔌 API Documentation

### Base URL

```
http://localhost:8000/api
```

### Endpoints

#### Get All Scans

```http
GET /scans
```

**Query Parameters:**
- `limit` (int, default: 50) - Number of records
- `offset` (int, default: 0) - Skip records
- `risk_level` (string, optional) - Filter by risk level

**Response:**
```json
{
  "total": 11,
  "scans": [
    {
      "id": 1,
      "zone_id": "A-01",
      "latitude": 34.2257,
      "longitude": -117.8512,
      "avg_air_temp": 29.43,
      "avg_humidity": 62.5,
      "avg_plant_temp": 33.5,
      "fuel_load": 0.3801,
      "risk_level": "medium",
      "completed_at": "2026-01-30T20:18:00"
    }
  ]
}
```

#### Get Scan Details

```http
GET /scans/{scan_id}
```

**Response:**
```json
{
  "id": 1,
  "zone_id": "A-01",
  "latitude": 34.2257,
  "longitude": -117.8512,
  "avg_plant_temp": 33.5,
  "fuel_load": 0.3801,
  "images": [...]
}
```

#### Get Heatmap Data

```http
GET /scans/{scan_id}/heatmap-data
```

**Response:**
```json
{
  "scan_id": 1,
  "total_points": 400,
  "data_points": [
    {
      "latitude": 34.22442945,
      "longitude": -117.85086962,
      "air_temperature": 30.61,
      "air_humidity": 59.13,
      "plant_temperature": 34.5,
      "one_hour_fuel": 0.0298,
      "ten_hour_fuel": 0.1268,
      "hundred_hour_fuel": 0.2451,
      "fire_risk": 0.3892
    }
  ]
}
```

---

## 🗺️ Heatmap System

### Implementation

The heatmap system uses **ImageOverlay** with **bilinear interpolation** for smooth gradient visualization.

#### Key Components

1. **`SimpleHeatmap.jsx`**
   - Generates 512×512 high-resolution heatmap image
   - Applies bilinear interpolation between grid points
   - Renders as ImageOverlay on Leaflet map

2. **Bilinear Interpolation Algorithm**

```javascript
function bilinearInterpolate(x, y, gridData) {
  // Find surrounding 4 grid points
  const col0 = Math.floor(x);
  const row0 = Math.floor(y);
  const col1 = col0 + 1;
  const row1 = row0 + 1;
  
  // Get fractional parts
  const dx = x - col0;
  const dy = y - row0;
  
  // Get values at corners
  const v00 = gridData[row0][col0];
  const v10 = gridData[row0][col1];
  const v01 = gridData[row1][col0];
  const v11 = gridData[row1][col1];
  
  // Interpolate
  const top = v00 * (1 - dx) + v10 * dx;
  const bottom = v01 * (1 - dx) + v11 * dx;
  return top * (1 - dy) + bottom * dy;
}
```

3. **Color Gradient**

```javascript
const colorStops = [
  { pos: 0.0, color: '#0000ff' },   // Blue (low)
  { pos: 0.25, color: '#00ffff' },  // Cyan
  { pos: 0.5, color: '#00ff00' },   // Green
  { pos: 0.65, color: '#ffff00' },  // Yellow
  { pos: 0.8, color: '#ff8000' },   // Orange
  { pos: 1.0, color: '#ff0000' }    // Red (high)
];
```

### Features

- **Fixed Zoom Level**: Locked at zoom 20 for consistency
- **Dual Boundaries**: 50m (scan area) and 200m (robot range)
- **Layer Switching**: 7 different data layers
- **Real-time Updates**: Instant layer switching
- **High Resolution**: 400 measurement points per scan

---

## 📊 Data Generation

### Generate Test Data

```bash
cd backend

# Generate 20×20 grid with 400 points per scan
python generate_ultra_dense_grid.py
```

**Configuration:**
- Grid Size: 20 × 20 = 400 points
- Point Spacing: 2.5 meters
- Coverage: 47.5m × 47.5m (within 50m boundary)
- Data Pattern: Sine wave gradients for smooth transitions

### Update Aggregate Statistics

```bash
cd backend

# Calculate and update statistics for all scans
python update_scan_aggregates.py
```

**Calculates:**
- Average ground temperature
- Average air temperature
- Average humidity
- Total fuel load (sum of 1h, 10h, 100h fuels)
- Temperature differential

---

## 🔧 Troubleshooting

### Backend Issues

#### Database Connection Error

**Problem**: `Can't connect to MySQL server`

**Solution**:
```bash
# Check MySQL is running
mysql -u root -p

# Verify .env configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pyroscope_db
```

#### Missing email-validator Module

**Problem**: `ImportError: email-validator is not installed`

**Solution**:
```bash
# Activate virtual environment
cd backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate    # Linux/Mac

# Install missing dependency
pip install email-validator

# Restart backend
python -m uvicorn app.main:app --reload
```

#### Migration Errors

**Problem**: `Incorrect DECIMAL value`

**Solution**:
```bash
# Reset migrations
cd backend
alembic downgrade base
alembic upgrade head
```

#### PowerShell cURL Not Working

**Problem**: `A parameter cannot be found that matches parameter name 'X'`

**Cause**: PowerShell's `curl` doesn't support standard syntax

**Solution**: Use Python test script instead:
```bash
cd test
..\backend\venv\Scripts\python.exe upload_test.py
```

### Frontend Issues

#### Heatmap Not Displaying

**Solution**:
1. Check browser console for errors (F12)
2. Verify API is returning data:
   ```bash
   curl http://localhost:8000/api/scans/1/heatmap-data
   ```
3. Clear browser cache and reload (Ctrl+Shift+R)

#### Data Not Updating

**Solution**:
1. Restart backend server
2. Clear browser cache
3. Check API response in Network tab (F12)

### Common Fixes

```bash
# Restart backend
cd backend
# Ctrl+C to stop
python -m uvicorn app.main:app --reload

# Reinstall frontend dependencies
npm install

# Clear npm cache
npm cache clean --force
```

---

## 📈 Performance

### Optimization Features

- **Canvas Rendering**: Direct pixel manipulation for speed
- **Image Caching**: Pre-rendered heatmap images
- **Lazy Loading**: Components load on demand
- **Database Indexing**: Optimized queries
- **Connection Pooling**: Efficient database connections

### Metrics

- **Heatmap Generation**: ~200ms
- **API Response Time**: <100ms
- **Page Load**: <1 second
- **Layer Switch**: Instant

---

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Style

- **Python**: Follow PEP 8
- **JavaScript**: ESLint + Prettier
- **Commits**: Conventional Commits format

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Team

- **Development**: Pyroscope Team
- **Institution**: Fire Risk Research Lab
- **Contact**: pyroscope@example.com

---

## 🙏 Acknowledgments

- Leaflet mapping library
- FastAPI framework
- React community
- Open source contributors

---

## 📚 Additional Resources

- [API Documentation](./docs/API.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Heatmap Implementation](./INTERPOLATED_HEATMAP_IMPLEMENTATION.md)
- [Troubleshooting Guide](./DEBUG_HEATMAP.md)

---

**Last Updated**: February 17, 2026

**Version**: 1.0.0

**Status**: Production Ready ✅

# Pyroscope Dashboard - 火灾风险监控系统

使用自主机器人进行环境数据收集和分析的综合性野火风险监控和预测系统。

## 🚀 快速启动

### 环境要求

- **Python 3.8+** （后端）
- **Node.js 16+** （前端）
- **MySQL 8.0+** （数据库）

### 启动应用程序

#### 1. 启动后端服务器

```bash
# 进入后端目录
cd backend

# 激活虚拟环境（如果使用）
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# 启动 FastAPI 服务器
python -m uvicorn app.main:app --reload
```

后端运行地址：**http://localhost:8000**

#### 2. 启动前端开发服务器

```bash
# 在新终端中，进入项目根目录
cd pyroscope_dashboard

# 启动 Vite 开发服务器
npm run dev
```

前端运行地址：**http://localhost:5173**

---

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [安装步骤](#安装步骤)
- [项目结构](#项目结构)
- [配置说明](#配置说明)
- [数据库设置](#数据库设置)
- [API 文档](#api-文档)
- [热力图系统](#热力图系统)
- [数据生成](#数据生成)
- [故障排除](#故障排除)
- [贡献指南](#贡献指南)

---

## ✨ 功能特性

### 核心功能

- **实时环境监控**
  - 空气温度和湿度
  - 地表温度测量
  - 风速跟踪
  - 基于 GPS 的位置跟踪

- **高级热力图可视化**
  - 7 个交互式热力图图层
  - 双线性插值实现平滑渐变
  - 多种燃料负荷指标
  - 集成火灾风险评估

- **自主扫描**
  - 50m × 50m 扫描区域覆盖
  - 20 × 20 测量网格（400 个点）
  - 2.5m 点间距，高分辨率
  - 自动化数据收集

- **火灾风险分析**
  - 实时风险计算
  - 多因素评估（温度、湿度、燃料）
  - 历史趋势分析
  - 风险等级分类

### 热力图图层

1. **地表温度** - 表面温度分布
2. **空气温度** - 大气温度模式
3. **空气湿度** - 湿度水平映射
4. **1 小时燃料** - 快速燃烧植被
5. **10 小时燃料** - 中速燃烧材料
6. **100 小时燃料** - 慢速燃烧大型燃料
7. **火灾风险** - 整体火灾危险评估

---

## 🛠 技术栈

### 前端

- **框架**: React 18
- **构建工具**: Vite
- **地图库**: Leaflet + React-Leaflet
- **UI 组件**: Lucide React Icons
- **样式**: CSS3 with CSS Variables

### 后端

- **框架**: FastAPI (Python)
- **数据库**: MySQL 8.0
- **ORM**: SQLAlchemy
- **验证**: Pydantic
- **迁移**: Alembic
- **网络爬虫**: Selenium（用于燃料估算）

### 数据处理

- **插值**: 双线性插值算法
- **可视化**: Canvas 2D + ImageOverlay
- **数据生成**: NumPy + 正弦波算法

---

## 📦 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/your-repo/pyroscope_dashboard.git
cd pyroscope_dashboard
```

### 2. 后端设置

#### 安装 Python 依赖

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 配置环境变量

在 `backend/` 目录创建 `.env` 文件：

```env
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pyroscope_db
DB_USER=your_username
DB_PASSWORD=your_password

# API 配置
API_PORT=8000
DEBUG=True

# 燃料估算 API（可选）
FUEL_ESTIMATION_API_URL=https://www.wfas.net/nfdr-fuel-moisture/
FUEL_ESTIMATION_TIMEOUT=60
FUEL_ESTIMATION_HEADLESS=True
```

#### 设置数据库

```bash
# 访问 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE pyroscope_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 运行迁移
cd backend
alembic upgrade head
```

### 3. 前端设置

```bash
# 进入项目根目录
cd pyroscope_dashboard

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

## 📁 项目结构

```
pyroscope_dashboard/
├── backend/
│   ├── app/
│   │   ├── models/          # 数据库模型
│   │   │   ├── scan.py      # 扫描记录
│   │   │   ├── environmental.py  # 环境数据
│   │   │   └── image.py     # 图像记录
│   │   ├── routers/         # API 端点
│   │   │   ├── scans.py     # 扫描操作
│   │   │   └── images.py    # 图像处理
│   │   ├── schemas/         # Pydantic 模式
│   │   │   ├── scan.py
│   │   │   ├── environmental.py
│   │   │   └── heatmap.py
│   │   ├── services/        # 业务逻辑
│   │   │   ├── scan_service.py
│   │   │   └── fire_risk_service.py
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # FastAPI 应用
│   ├── alembic/             # 数据库迁移
│   ├── generate_ultra_dense_grid.py  # 数据生成
│   ├── update_scan_aggregates.py     # 统计更新
│   └── requirements.txt
├── src/
│   ├── components/
│   │   ├── HeatmapPanel.jsx      # 主热力图组件
│   │   ├── SimpleHeatmap.jsx     # 插值热力图
│   │   ├── ScanResults.jsx       # 详细扫描视图
│   │   ├── DataLog.jsx           # 数据表格
│   │   ├── Sidebar.jsx           # 左侧边栏
│   │   └── Map.jsx               # 主地图
│   ├── services/
│   │   └── api.js                # API 客户端
│   ├── App.jsx                   # 主应用
│   └── main.jsx                  # 入口点
├── public/                  # 静态资源
├── package.json
└── vite.config.js
```

---

## ⚙️ 配置说明

### 数据库模式

#### `scan_records` 表

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

#### `environmental_data` 表

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

## 🔌 API 文档

### 基础 URL

```
http://localhost:8000/api
```

### 端点

#### 获取所有扫描

```http
GET /scans
```

**查询参数：**
- `limit` (int, 默认: 50) - 记录数量
- `offset` (int, 默认: 0) - 跳过记录
- `risk_level` (string, 可选) - 按风险等级过滤

**响应：**
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

#### 获取扫描详情

```http
GET /scans/{scan_id}
```

**响应：**
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

#### 获取热力图数据

```http
GET /scans/{scan_id}/heatmap-data
```

**响应：**
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

## 🗺️ 热力图系统

### 实现方式

热力图系统使用 **ImageOverlay** 配合 **双线性插值** 实现平滑渐变可视化。

#### 关键组件

1. **`SimpleHeatmap.jsx`**
   - 生成 512×512 高分辨率热力图图像
   - 在网格点之间应用双线性插值
   - 在 Leaflet 地图上渲染为 ImageOverlay

2. **双线性插值算法**

```javascript
function bilinearInterpolate(x, y, gridData) {
  // 找到周围的 4 个网格点
  const col0 = Math.floor(x);
  const row0 = Math.floor(y);
  const col1 = col0 + 1;
  const row1 = row0 + 1;
  
  // 获取小数部分
  const dx = x - col0;
  const dy = y - row0;
  
  // 获取四个角的值
  const v00 = gridData[row0][col0];
  const v10 = gridData[row0][col1];
  const v01 = gridData[row1][col0];
  const v11 = gridData[row1][col1];
  
  // 插值计算
  const top = v00 * (1 - dx) + v10 * dx;
  const bottom = v01 * (1 - dx) + v11 * dx;
  return top * (1 - dy) + bottom * dy;
}
```

3. **颜色渐变**

```javascript
const colorStops = [
  { pos: 0.0, color: '#0000ff' },   // 蓝色（低）
  { pos: 0.25, color: '#00ffff' },  // 青色
  { pos: 0.5, color: '#00ff00' },   // 绿色
  { pos: 0.65, color: '#ffff00' },  // 黄色
  { pos: 0.8, color: '#ff8000' },   // 橙色
  { pos: 1.0, color: '#ff0000' }    // 红色（高）
];
```

### 功能特点

- **固定缩放级别**：锁定在 zoom 20 以保持一致性
- **双层边界**：50m（扫描区域）和 200m（机器人范围）
- **图层切换**：7 个不同的数据图层
- **实时更新**：图层切换即时响应
- **高分辨率**：每次扫描 400 个测量点

---

## 📊 数据生成

### 生成测试数据

```bash
cd backend

# 生成 20×20 网格，每次扫描 400 个点
python generate_ultra_dense_grid.py
```

**配置：**
- 网格大小：20 × 20 = 400 点
- 点间距：2.5 米
- 覆盖范围：47.5m × 47.5m（在 50m 边界内）
- 数据模式：正弦波渐变实现平滑过渡

### 更新聚合统计

```bash
cd backend

# 计算并更新所有扫描的统计数据
python update_scan_aggregates.py
```

**计算内容：**
- 平均地表温度
- 平均空气温度
- 平均湿度
- 总燃料负荷（1h、10h、100h 燃料之和）
- 温度差

---

## 🔧 故障排除

### 后端问题

#### 数据库连接错误

**问题**：`Can't connect to MySQL server`

**解决方案**：
```bash
# 检查 MySQL 是否运行
mysql -u root -p

# 验证 .env 配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pyroscope_db
```

#### 缺少 email-validator 模块

**问题**：`ImportError: email-validator is not installed`

**解决方案**：
```bash
# 激活虚拟环境
cd backend
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate    # Linux/Mac

# 安装缺失的依赖
pip install email-validator

# 重启后端
python -m uvicorn app.main:app --reload
```

#### 迁移错误

**问题**：`Incorrect DECIMAL value`

**解决方案**：
```bash
# 重置迁移
cd backend
alembic downgrade base
alembic upgrade head
```

#### PowerShell 中 cURL 命令不工作

**问题**：`A parameter cannot be found that matches parameter name 'X'`

**原因**：PowerShell 的 `curl` 不支持标准语法

**解决方案**：改用 Python 测试脚本：
```bash
cd test
..\backend\venv\Scripts\python.exe upload_test.py
```

### 前端问题

#### 热力图不显示

**解决方案**：
1. 检查浏览器控制台错误（F12）
2. 验证 API 是否返回数据：
   ```bash
   curl http://localhost:8000/api/scans/1/heatmap-data
   ```
3. 清除浏览器缓存并重新加载（Ctrl+Shift+R）

#### 数据不更新

**解决方案**：
1. 重启后端服务器
2. 清除浏览器缓存
3. 检查 Network 标签中的 API 响应（F12）

### 常见修复

```bash
# 重启后端
cd backend
# Ctrl+C 停止
python -m uvicorn app.main:app --reload

# 重新安装前端依赖
npm install

# 清除 npm 缓存
npm cache clean --force
```

---

## 📈 性能

### 优化特性

- **Canvas 渲染**：直接像素操作提高速度
- **图像缓存**：预渲染的热力图图像
- **懒加载**：按需加载组件
- **数据库索引**：优化查询
- **连接池**：高效的数据库连接

### 性能指标

- **热力图生成**：~200ms
- **API 响应时间**：<100ms
- **页面加载**：<1 秒
- **图层切换**：即时

---

## 🤝 贡献指南

### 开发流程

1. Fork 仓库
2. 创建功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交更改（`git commit -m 'Add AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开 Pull Request

### 代码风格

- **Python**：遵循 PEP 8
- **JavaScript**：ESLint + Prettier
- **提交**：Conventional Commits 格式

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

---

## 👥 团队

- **开发**：Pyroscope 团队
- **机构**：火灾风险研究实验室
- **联系**：pyroscope@example.com

---

## 🙏 致谢

- Leaflet 地图库
- FastAPI 框架
- React 社区
- 开源贡献者

---

## 📚 其他资源

- [API 文档](./docs/API.md)
- [部署指南](./DEPLOYMENT_GUIDE.md)
- [热力图实现](./INTERPOLATED_HEATMAP_IMPLEMENTATION.md)
- [故障排除指南](./DEBUG_HEATMAP.md)

---

**最后更新**：2026年2月17日

**版本**：1.0.0

**状态**：生产就绪 ✅

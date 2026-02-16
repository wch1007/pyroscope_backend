# Fuel Load Estimation Integration Guide

## 概述

本系统集成了 Wildlands AI 的燃料负载估算功能（https://fe.wildlands.ai/），可以自动分析上传的图片并估算燃料负载数据。

## 功能特性

- ✅ 自动燃料负载估算（基于上传的可见光图片）
- ✅ 详细的燃料分类数据（1小时、10小时、100小时燃料）
- ✅ 松果数量统计
- ✅ 异步处理，不阻塞图片上传
- ✅ 自动更新扫描记录数据
- ✅ 前端实时展示估算结果

## 技术实现

### 后端架构

1. **Selenium WebDriver 自动化**
   - 使用 Selenium 控制 Chrome 浏览器
   - 自动访问 Wildlands AI 网站
   - 上传图片并获取估算结果

2. **数据库扩展**
   - 新增字段：`one_hour_fuel`, `ten_hour_fuel`, `hundred_hour_fuel`, `pine_cone_count`
   - 修改字段：`fuel_load` (String → DECIMAL(10,4))

3. **API 端点增强**
   - `/api/images/upload` - 上传图片时自动触发燃料估算
   - 新增参数：`estimate_fuel` (默认: true)
   - 响应包含：`fuel_estimation` 对象

### 前端展示

- 扫描结果页面显示详细的燃料估算数据
- 突出显示总燃料负载
- 分类显示各类型燃料数据
- 松果数量统计

## 安装步骤

### 1. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

新增依赖：
- `selenium==4.27.1` - 浏览器自动化
- `webdriver-manager==4.0.2` - 自动管理 ChromeDriver
- `httpx==0.27.2` - HTTP 客户端（备用）

### 2. 安装 Chrome 浏览器

确保系统已安装 Google Chrome 浏览器。如果使用无头模式（headless），不需要图形界面。

### 3. 配置环境变量

复制 `.env.example` 到 `.env` 并配置：

```bash
cp .env.example .env
```

关键配置项：
```
FUEL_ESTIMATION_API_URL=https://fe.wildlands.ai/
FUEL_ESTIMATION_TIMEOUT=60              # 超时时间（秒）
FUEL_ESTIMATION_HEADLESS=True           # 无头模式
```

### 4. 运行数据库迁移

```bash
cd backend
alembic upgrade head
```

这将执行迁移 `003_add_fuel_estimation_fields.py`，添加新的数据库字段。

### 5. 启动后端服务

```bash
cd backend
python run.py
```

后端将在 `http://localhost:8000` 启动。

### 6. 启动前端服务

```bash
npm install
npm run dev
```

前端将在 `http://localhost:5173` 启动。

## 使用方法

### API 使用示例

#### 上传图片并自动估算燃料

```bash
curl -X POST "http://localhost:8000/api/images/upload" \
  -F "scan_id=1" \
  -F "image_type=visible" \
  -F "file=@/path/to/image.jpg" \
  -F "estimate_fuel=true"
```

**响应示例：**

```json
{
  "image_id": 123,
  "file_path": "uploads/visible/2026/02/14/image.jpg",
  "url": "/api/images/123",
  "message": "Image uploaded successfully",
  "fuel_estimation": {
    "total_fuel_load": 0.165,
    "one_hour_fuel": 0.021,
    "ten_hour_fuel": 0.082,
    "hundred_hour_fuel": 0.062,
    "pine_cone_count": 1
  }
}
```

#### 禁用燃料估算

如果不需要燃料估算，可以设置 `estimate_fuel=false`：

```bash
curl -X POST "http://localhost:8000/api/images/upload" \
  -F "scan_id=1" \
  -F "image_type=thermal" \
  -F "file=@/path/to/image.jpg" \
  -F "estimate_fuel=false"
```

### 前端使用

1. 创建新的扫描记录
2. 上传可见光图片（image_type=visible）
3. 系统自动调用 Wildlands AI API 进行燃料估算
4. 在扫描结果页面查看详细的燃料估算数据

## 数据模型

### ScanRecord 模型

新增字段：

| 字段名 | 类型 | 描述 | 单位 |
|--------|------|------|------|
| `fuel_load` | DECIMAL(10,4) | 总燃料负载 | tons/acre |
| `one_hour_fuel` | DECIMAL(10,4) | 1小时燃料 | tons/acre |
| `ten_hour_fuel` | DECIMAL(10,4) | 10小时燃料 | tons/acre |
| `hundred_hour_fuel` | DECIMAL(10,4) | 100小时燃料 | tons/acre |
| `pine_cone_count` | Integer | 松果数量 | 个 |

## 性能优化建议

### 1. 异步处理（推荐用于生产环境）

当前实现是同步的，可能导致图片上传响应时间较长（30-60秒）。

**改进方案：**
- 使用 Celery 或 RQ 任务队列
- 后台异步处理燃料估算
- 通过 WebSocket 或轮询通知前端

### 2. 缓存机制

避免重复分析相同的图片：
- 基于图片哈希值缓存估算结果
- 减少对外部 API 的调用次数

### 3. 并行处理

如果上传多张图片：
- 使用线程池并行处理
- 提高整体处理速度

## 故障排除

### Chrome/ChromeDriver 问题

**问题：** `WebDriver initialization failed`

**解决方案：**
1. 确保已安装 Chrome 浏览器
2. 检查 Chrome 版本与 ChromeDriver 版本兼容性
3. 手动安装 ChromeDriver：
   ```bash
   pip install webdriver-manager --upgrade
   ```

### 超时问题

**问题：** `Timeout waiting for elements`

**解决方案：**
1. 增加超时时间：`FUEL_ESTIMATION_TIMEOUT=120`
2. 检查网络连接
3. 确认 https://fe.wildlands.ai/ 可访问

### 结果解析失败

**问题：** `Failed to parse fuel estimation results`

**解决方案：**
1. 检查日志中的页面文本内容
2. Wildlands AI 网站可能更新了页面结构
3. 更新 `fuel_estimation_service.py` 中的选择器

### 无头模式问题

**问题：** 无头模式下无法正常工作

**解决方案：**
1. 临时禁用无头模式：`FUEL_ESTIMATION_HEADLESS=False`
2. 观察浏览器实际操作过程
3. 调试定位问题

## 限制和注意事项

1. **仅支持可见光图片**
   - 燃料估算只对 `image_type=visible` 生效
   - 热成像图片不会触发估算

2. **网络依赖**
   - 需要稳定的互联网连接
   - 依赖外部 API 的可用性

3. **处理时间**
   - 每张图片估算需要 30-60 秒
   - 同步处理会增加响应时间

4. **浏览器资源**
   - 每次估算都会启动新的浏览器实例
   - 消耗一定的系统资源

5. **API 使用限制**
   - Wildlands AI 可能有速率限制
   - 建议在生产环境中添加重试和限流机制

## 未来改进

- [ ] 实现异步任务队列（Celery）
- [ ] 添加结果缓存机制
- [ ] 支持批量图片处理
- [ ] 添加估算进度通知
- [ ] 实现错误重试机制
- [ ] 添加单元测试和集成测试
- [ ] 监控和日志记录优化

## 相关文件

### 后端文件
- `backend/app/services/fuel_estimation_service.py` - 燃料估算服务
- `backend/app/routers/images.py` - 图片上传路由（集成估算）
- `backend/app/models/scan.py` - 数据模型
- `backend/app/schemas/scan.py` - 数据验证模型
- `backend/app/schemas/image.py` - 图片响应模型
- `backend/app/config.py` - 配置管理
- `backend/alembic/versions/003_add_fuel_estimation_fields.py` - 数据库迁移

### 前端文件
- `src/services/api.js` - API 客户端
- `src/components/ScanResults.jsx` - 扫描结果展示
- `src/components/ScanResults.css` - 样式文件

## 技术支持

如有问题，请查看：
1. 后端日志：`backend/logs/`
2. Selenium 截图（如果启用）
3. 浏览器控制台输出

## 版权声明

燃料估算功能由 [Wildlands AI](https://allenai.org/wildlands) 提供，属于 Allen Institute for AI (AI2) 项目。

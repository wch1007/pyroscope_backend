# 🚀 燃料负载估算功能快速启动指南

## 5分钟快速上手

### 步骤 1：安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 步骤 2：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，确保包含以下配置
FUEL_ESTIMATION_API_URL=https://fe.wildlands.ai/
FUEL_ESTIMATION_TIMEOUT=60
FUEL_ESTIMATION_HEADLESS=True
```

### 步骤 3：运行数据库迁移

```bash
alembic upgrade head
```

### 步骤 4：测试燃料估算服务

```bash
python test_fuel_estimation.py
```

如果成功，您将看到类似以下的输出：

```
✅ Estimation Successful!

  🔥 Total Fuel Load:     0.165 tons/acre
  ⏱️  1-Hour Fuel:         0.021 tons/acre
  ⏱️  10-Hour Fuel:        0.082 tons/acre
  ⏱️  100-Hour Fuel:       0.062 tons/acre
  🌲 Pine Cone Count:     1
```

### 步骤 5：启动应用

```bash
# 启动后端
python run.py

# 在另一个终端启动前端
cd ..
npm install
npm run dev
```

### 步骤 6：使用功能

1. 访问 `http://localhost:5173`
2. 创建新的扫描记录
3. 上传可见光图片
4. 等待燃料估算完成（30-60秒）
5. 查看扫描结果页面的燃料估算数据

## 使用 API

### 上传图片并获取燃料估算

```bash
curl -X POST "http://localhost:8000/api/images/upload" \
  -F "scan_id=1" \
  -F "image_type=visible" \
  -F "file=@/path/to/your/image.jpg" \
  -F "estimate_fuel=true"
```

### 响应示例

```json
{
  "image_id": 1,
  "file_path": "uploads/visible/2026/02/14/image.jpg",
  "url": "/api/images/1",
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

## 常见问题

### Q: ChromeDriver 安装失败？
**A:** webdriver-manager 会自动下载 ChromeDriver。如果失败，请确保：
- 已安装 Google Chrome 浏览器
- 网络连接正常
- 尝试手动安装：`pip install webdriver-manager --upgrade`

### Q: 估算超时？
**A:** 增加超时时间：
```bash
# 在 .env 中设置
FUEL_ESTIMATION_TIMEOUT=120
```

### Q: 想看到浏览器操作过程？
**A:** 禁用无头模式：
```bash
# 在 .env 中设置
FUEL_ESTIMATION_HEADLESS=False
```

### Q: 只有特定图片类型会触发估算吗？
**A:** 是的，只有 `image_type=visible` 的图片会自动触发燃料估算。热成像图片不会触发。

## 性能提示

⚠️ **注意：** 当前实现是同步的，每次估算需要 30-60 秒。

**生产环境建议：**
- 使用异步任务队列（Celery）
- 实现后台处理
- 通过 WebSocket 实时推送结果

## 完整文档

详细的集成文档请参考：[FUEL_ESTIMATION_INTEGRATION.md](./FUEL_ESTIMATION_INTEGRATION.md)

## 技术栈

- 🐍 Python + FastAPI
- 🤖 Selenium WebDriver
- 🌐 Wildlands AI API
- 💾 MySQL 数据库
- ⚛️ React 前端

## 支持

如遇问题，请查看：
- 后端日志输出
- Chrome 浏览器版本兼容性
- 网络连接状态
- Wildlands AI 网站可访问性

# 后端启动脚本
# 使用方法: 在 PowerShell 中运行 .\START_BACKEND.ps1

Write-Host "================================" -ForegroundColor Green
Write-Host "启动 Pyroscope 后端服务" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# 1. 进入 backend 目录
Write-Host "[1/6] 进入 backend 目录..." -ForegroundColor Yellow
Set-Location -Path ".\backend"
Write-Host "当前目录: $PWD" -ForegroundColor Cyan
Write-Host ""

# 2. 安装依赖
Write-Host "[2/6] 安装 Python 依赖..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 依赖安装失败！" -ForegroundColor Red
    exit 1
}
Write-Host "✅ 依赖安装完成" -ForegroundColor Green
Write-Host ""

# 3. 检查 .env 文件
Write-Host "[3/6] 检查环境变量文件..." -ForegroundColor Yellow
if (!(Test-Path .env)) {
    Write-Host "未找到 .env 文件，从 .env.example 复制..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  请编辑 .env 文件，配置数据库连接信息！" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env 文件已存在" -ForegroundColor Green
}
Write-Host ""

# 4. 运行数据库迁移
Write-Host "[4/6] 运行数据库迁移..." -ForegroundColor Yellow
Write-Host "（这将添加燃料估算相关的数据库字段）" -ForegroundColor Cyan
alembic upgrade head
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  数据库迁移失败，请检查数据库连接配置" -ForegroundColor Yellow
} else {
    Write-Host "✅ 数据库迁移完成" -ForegroundColor Green
}
Write-Host ""

# 5. 询问是否测试燃料估算
Write-Host "[5/6] 是否测试燃料估算功能？(y/n)" -ForegroundColor Yellow
$test = Read-Host "输入选择"
if ($test -eq "y" -or $test -eq "Y") {
    Write-Host "运行测试..." -ForegroundColor Cyan
    python test_fuel_estimation.py
}
Write-Host ""

# 6. 启动服务
Write-Host "[6/6] 启动后端服务..." -ForegroundColor Yellow
Write-Host "服务将在 http://localhost:8000 启动" -ForegroundColor Cyan
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

python run.py

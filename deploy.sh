#!/bin/bash
set -e

echo "========================================"
echo "🚀 Araç Hasar Analizi Manuel Deploy Başlıyor..."
echo "========================================"

echo "📦 GitHub'dan yeni kodlar çekiliyor..."
git pull origin main

echo "🐳 Konteynerler yeniden inşa ediliyor..."
docker compose up -d --build --remove-orphans

echo "🧹 Eski sistem kalıntıları temizleniyor..."
docker image prune -f

# 🚨 Sadece Nginx ayar dosyalarında (conf) değişiklik yaparsan 
# aşağıdaki satırın başındaki '#' işaretini kaldırıp öyle çalıştır:
# sudo systemctl reload nginx

echo "========================================"
echo "✅ Manuel Deployment Başarıyla Tamamlandı!"
echo "========================================"

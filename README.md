# menu_buffet

## 🚀 ขั้นตอนการติดตั้ง

1. Clone Project
2. คัดลอกไฟล์ .env สำหรับ docker, backend, frontend
3. Run docker-compose build
4. Run docker-compose up -d
5. Run docker-compose exec backend alembic upgrade head
6. ถ้า ข้อ 5 error ให้ Run docker-compose exec backend alembic stamp head
7. Run docker-compose exec backend python seed.py
8. http://localhost:5173/
# VOICSKY Việt Nam

Node.js 24+. Cài dependency bằng `npm ci`, chạy `npm run dev`, mở http://127.0.0.1:3000. `npm run build` và `npm start` cho production local. `npm test` kiểm tra commerce.

Đọc docs/voicsky-clone/spec.md trước khi thay đổi. Media nằm trong public/assets; HTML nguồn bản địa hóa trong data/pages. `python scripts/capture.py` thu thập lại nguồn (requests, beautifulsoup4), `python scripts/translate.py` tạo bản dịch máy qua Google Translate, `python scripts/finalize.py` áp dụng sửa lỗi và báo cáo. Capture lại sẽ ghi đè HTML đã dịch; cần chạy lại translate/finalize theo thứ tự.

Đây là bản clone khảo sát với commerce demo, chưa sẵn sàng nhận thanh toán thật. Source HTML được phục vụ bởi Next Route Handler, chưa chuyển thành hệ component React. Các giới hạn dữ liệu và phần cần hoàn thiện được ghi rõ trong hồ sơ bàn giao.

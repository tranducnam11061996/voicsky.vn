# Bàn giao database phase sau

1. Import Asset theo source_url/local_path; đối chiếu SHA256 và gộp bytes giống nhau, giữ alias URL.
2. Import Product theo handle và source URL; Shopify ID và variant ID luôn string.
3. Import các option/value đúng thứ tự, sau đó 43 variant theo tổ hợp nguồn. Không tự thêm tổ hợp.
4. data/sections.json đã có 120 section có owner, order, type, heading và HTML. Còn cần tách HTML thành trường riêng theo từng loại module khi gắn CMS.
5. data/specifications.json đã có 537 dòng với nhóm tab, label/value/order; cần duyệt bản dịch và tách đơn vị nếu database yêu cầu.
6. data/partners.json có 30 đối tác; data/locations.json có 105 record địa điểm. UI nguồn hiển thị 103: giữ nguyên record để phase sau rà soát trùng, không xóa nhằm ép khớp số đếm. Địa chỉ/tên riêng giữ tiếng Anh nguồn.
7. Chuyển translations sang entity/field/locale và duyệt bản dịch. Bảo tồn tiếng Anh từ dữ liệu sản phẩm và có thể chạy lại capture nguồn.
8. Thay repository đọc JSON bằng adapter database. Giữ contract catalog cho client; thêm adapter commerce server cho giá/tồn kho/đơn thật.

Không import public/runtime/commerce.js, localStorage, sessionStorage, giá fixture, receipt demo hoặc bài demo thành dữ liệu sản xuất. Price chuẩn hóa để null; dữ liệu nguồn giá 0 không được coi là giá Việt Nam. Không import token, tracking Shopify hoặc script analytics.

Cần dữ liệu từ chủ website khi phase vận hành: pháp nhân/liên hệ Việt Nam, giá thật, SKU Việt Nam, tồn kho, điểm bán Việt Nam, vận chuyển/thuế, policy, nội dung tin tức. Không có dữ liệu này trong nguồn khảo sát.

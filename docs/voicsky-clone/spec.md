# VOICSKY Việt Nam — đặc tả và hiện trạng

Ngày chốt: 2026-11-17. Nguồn: https://voicsky.com/en-my. Website tiếng Việt, font Be Vietnam Pro, tên model giữ nguyên, media nguồn lưu local. Next.js/TypeScript phục vụ các route, catalog qua repository; thương mại dùng fixture riêng.

## Phạm vi
Trang chủ, 5 collection, 12 sản phẩm với 43 biến thể, contact, where-to-buy, sự kiện, preorder, News, hai policy; bổ sung about, bài minh họa, search, cart, checkout, receipt và 404. Xem route-matrix.csv.

## Thiết kế
Giữ markup/CSS/custom elements công khai của nguồn để bảo toàn hero video, mega menu, carousel, accordion cấu tạo, audio và tab thông số. Accent #67c9ff; sáng #f5f5f7, tối #161616; radius 20–24; mobile dưới 750px. Nội dung tiếng Việt dùng Be Vietnam Pro; tên model dùng font nguồn. Media có chữ tiếng Anh giữ nguyên. Hero 14 giây/slide, có điều khiển dừng và chuyển. Product có trạng thái hero và thông tin qua Discover; điều hướng section sticky.

## Thương mại demo
Giá bàn phím 1.490.000, chuột 790.000, lót chuột 990.000 VND. Tồn kho 10/biến thể, vận chuyển 30.000. Cùng variant gộp, khác variant tách dòng. Giỏ localStorage voicsky.cart.v1, receipt sessionStorage voicsky.receipt. Checkout bắt buộc tên, điện thoại, tỉnh/thành, phường/xã, địa chỉ; email tùy chọn. Chỉ COD mô phỏng. Không gửi đơn hoặc nhận tiền thật. Nguồn giá 0/available=false không được diễn giải là hàng miễn phí.

## Kiến trúc thực tế
Next.js Route Handler phục vụ HTML được chụp và bản địa hóa; custom elements nguồn giữ phần tương tác. lib/repositories.ts cung cấp ContentRepository và CatalogRepository. Runtime commerce tách khỏi dữ liệu nguồn. Đây là thay đổi so với phương án React Server Components của kế hoạch: ưu tiên độ trung thực khi tái sử dụng cấu trúc nguồn. Các section hiện lưu HTML; chưa chuyển toàn bộ thành React component hay entity quan hệ.

## Nội dung
Bản dịch máy lưu trong data/translations.json; cần biên tập trước production. News nguồn rỗng. /blogs/news/demo là nội dung minh họa, không phải tin chính thức. About chỉ dùng thông tin sản phẩm có nguồn. Policy là bản dịch nguồn Shopify, cần thay nội dung vận hành khi phát hành thật. AETHER là liên kết ngoài.

## Nghiệm thu
Build/typecheck và test commerce. Kiểm tra route, media local, variant, search có/không dấu, giỏ refresh, checkout sai/đúng, duplicate submit. So sánh desktop/mobile với slide và video đã cố định. Chưa tuyên bố đạt sai lệch hình học 4px khi chưa có bộ ảnh đối chiếu tự động. Xem acceptance-checklist.md và source-audit.md.

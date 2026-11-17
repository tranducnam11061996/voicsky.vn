# Sổ quan sát nguồn

Observed: root chuyển en-my; Shopify; 12 sản phẩm/43 biến thể; toàn bộ giá 0, không khả dụng; sitemap có News nhưng rỗng; /pages/about 404; browser /cart trở về home. Where-to-buy hiển thị 30 đối tác/103 địa điểm. Source scripts/CSS dùng Outfit và Gridular. Font Outfit có nhiều glyph tiếng Việt fallback trong phép đo browser.

Observed runtime: Discover đổi hero sang thông tin; accordion cấu tạo đổi ảnh; tab technical hiện bảng tương ứng; search Enter chuyển sang truy vấn title của Shopify; mobile menu và footer dùng accordion. Nguồn có lỗi custom element khi track null, bản local thêm guard.

Inferred: source là website giới thiệu sản phẩm và dẫn tới đại lý trong market quan sát. Không suy diễn checkout thật từ các script chung Shopify.

Unknown: checkout thật, đơn hàng thật, nghiệp vụ giá/thuế/vận chuyển. Không submit dữ liệu trên nguồn.

Ranh giới: đã đọc HTML của tất cả sản phẩm, không thao tác hết 43 tổ hợp. Cần rà soát nội dung mâu thuẫn CLOUDY Clicky/tactile. Không có REA Evidence ID: browser runtime dùng Chrome DevTools managed theo policy. Dữ liệu nguồn gồm URL từng sản phẩm; manifest chứa URL và SHA256 tài nguyên.

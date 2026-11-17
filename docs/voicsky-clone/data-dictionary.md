# Từ điển dữ liệu

data/products.json: product.id/handle string ổn định; name string; category keyboard/mouse/mouse-pad; image local URL; source_url provenance; price null khi chưa biết; source_price giữ 0 nguồn; variants là các tổ hợp thực tế, không nhân Cartesian; sections gồm source id và HTML.

variants.id là Shopify ID; phải chuyển sang string khi import database. options giữ thứ tự nguồn. sku có thể null. featured_image.src là URL nguồn, cần nối qua asset manifest. available/price trong variant là dữ liệu nguồn, không phải thông tin bán hàng Việt Nam.

data/translations.json: khóa là chuỗi tiếng Anh, giá trị là bản dịch máy tiếng Việt. Cần chuyển thành record theo entity/field/locale khi gắn CMS; không dùng bản dịch làm khóa quan hệ.

data/asset-manifest.json: source_url, local_path, status, bytes, sha256, mime, error nếu tải lỗi. Hash áp dụng bytes local; CSS/JS đã rewrite nên không phải digest bytes gốc.

data/pages/*.html: snapshot đã rewrite và dịch để phục vụ hiển thị. Không import nguyên trang thành bảng sản phẩm. Section HTML hiện chưa được chuẩn hóa thành trường nội dung độc lập.

Bổ sung: sections.json (120), specifications.json (537), asset-usages.json (575), partners.json (30), locations.json (105). Mỗi record có owner/product/partner key, order và nguồn theo entity liên quan. Bản dịch là máy dịch, chưa biên tập. Manifest cuối: 1.922 tài nguyên đã tải, 2 template expression bị loại. Ba ảnh icon Leaflet bổ sung từ package leaflet 1.9.4 trên unpkg, có resolved_source_url.

# TWeb - Email Gia Hạn Dịch Vụ Hosting (Odoo 17)

Mẫu email nhắc gia hạn dịch vụ hosting/domain **có bảng chi tiết dịch vụ**, khắc phục
hạn chế của email báo giá mặc định trong Odoo (chỉ in tổng tiền dạng văn xuôi,
không lặp qua `order_line`).

| | |
|---|---|
| **Tên kỹ thuật** | `tweb_hosting_renewal_mail` |
| **Phiên bản** | 17.0.1.1.0 |
| **Tác giả** | NGUYEN VAN TINH |
| **Email** | tinhnguyenvan91@gmail.com |
| **Điện thoại** | 0909977920 |
| **Website** | https://tweb.com.vn/ |
| **License** | LGPL-3 |
| **Phụ thuộc** | `sale_management`, `mail` |

## 1. Cài đặt

```bash
cp -r tweb_hosting_renewal_mail /path/to/addons/
docker compose restart odoo
```

Apps → Update Apps List → tìm **TWeb - Email Gia Hạn Dịch Vụ Hosting** → Install.

Cập nhật khi có bản mới:

```bash
docker compose exec odoo odoo -u tweb_hosting_renewal_mail -d <db> --stop-after-init
```

## 2. Nội dung module

```
tweb_hosting_renewal_mail/
├── __manifest__.py
├── __init__.py
├── models/
│   └── sale_order.py            # 2 trường nhập tay + 1 trường tính + action gửi mail
├── data/
│   └── mail_template_data.xml   # mail.template: tweb_hosting_renewal_mail.mail_template_hosting_renewal
└── views/
    └── sale_order_views.xml     # form / list / search
```

**Trường thêm vào `sale.order`**

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `hosting_expiry_date` | Date | Nhập tay, có tracking |
| `hosting_renewal_note` | Char | Ghi chú tuỳ chọn (VD tên miền) |
| `hosting_days_left` | Integer (compute) | Âm = đã hết hạn, dùng đổi nội dung email |

## 3. Sử dụng

1. Mở đơn hàng đã xác nhận → điền **Ngày hết hạn dịch vụ** (dưới Payment Terms).
2. Bấm nút **Gửi mail gia hạn** trên thanh header → wizard soạn mail mở ra với
   nội dung đã render sẵn, sửa được trước khi gửi.
3. Lọc danh sách cần gửi: Sales → Orders → filter **Sắp hết hạn (30 ngày)** /
   **Đã hết hạn**, hoặc group theo **Tháng hết hạn**.

Email tự đổi nội dung theo `hosting_days_left`:
còn hạn → khung cảnh báo vàng; quá hạn → khung đỏ + tiêu đề `[KHẨN]`.

## 4. Cấu hình cần thiết

**Settings → Companies → công ty → tab Bank Accounts**: khai báo tài khoản ngân hàng.
Khối "Thông tin thanh toán" trong email lấy dữ liệu từ đây (ngân hàng, số tài khoản,
chủ tài khoản). Nếu để trống, email chỉ hiện dòng "vui lòng liên hệ bộ phận kinh doanh".

Nội dung chuyển khoản tự sinh dạng `Gia han S00052` để tiện đối soát sao kê.

## 5. Ghi chú kỹ thuật

- Template dùng `t-out` (Odoo 17 đã bỏ `t-esc` / `t-raw` trong mail template).
- Template khai báo `noupdate="1"` → sửa nội dung qua giao diện sẽ **không** bị ghi đè
  khi update module. Muốn nạp lại bản gốc: xoá template ở
  *Settings → Technical → Email Templates* rồi chạy `-u`.
- Bảng chi tiết xử lý cả `line_section` và `line_note` nên không vỡ layout khi
  báo giá có dòng tiêu đề nhóm.
- Đính kèm PDF báo giá: thêm vào record template
  `<field name="report_template_ids" eval="[(4, ref('sale.action_report_saleorder'))]"/>`
  (Odoo 17 dùng `report_template_ids`, không phải `report_template`).

## 6. Test nhanh

```python
# odoo shell -d <db>
so = env['sale.order'].browse(52)
so.hosting_expiry_date = '2026-08-20'
tpl = env.ref('tweb_hosting_renewal_mail.mail_template_hosting_renewal')
tpl.send_mail(so.id, force_send=True, email_layout_xmlid='mail.mail_notification_light')
env.cr.commit()
```

---
© 2026 NGUYEN VAN TINH — https://tweb.com.vn/

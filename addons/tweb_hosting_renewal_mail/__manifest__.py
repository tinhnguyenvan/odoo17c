# -*- coding: utf-8 -*-
{
    "name": "TWeb - Email Gia Hạn Dịch Vụ Hosting",
    "summary": "Mẫu email nhắc gia hạn dịch vụ hosting/domain chi tiết trên Sale Order",
    "description": """
TWeb - Email Gia Hạn Dịch Vụ Hosting
=====================================

Bổ sung cho phân hệ Sale một mẫu email nhắc gia hạn dịch vụ đầy đủ chi tiết,
khắc phục hạn chế của email báo giá mặc định (chỉ hiển thị tổng tiền dạng văn xuôi).

Tính năng
---------
* Thêm trường **Ngày hết hạn dịch vụ** và **Ghi chú gia hạn** trên đơn hàng (nhập tay).
* Mẫu email nhắc gia hạn với:

  - Bảng chi tiết từng dòng dịch vụ: tên, số lượng, đơn giá, thuế, thành tiền
  - Dòng tổng: tạm tính, thuế, tổng cộng cần thanh toán
  - Nội dung tự đổi theo trạng thái: sắp hết hạn (cảnh báo vàng) / đã hết hạn (cảnh báo đỏ)
  - Thông tin chuyển khoản lấy động từ tài khoản ngân hàng của công ty
  - Nội dung chuyển khoản tự sinh theo mã đơn hàng để dễ đối soát
  - Nút dẫn tới cổng thông tin khách hàng (portal)

* Nút **Gửi mail gia hạn** trên đơn hàng đã xác nhận.
* Bộ lọc **Sắp hết hạn (30 ngày)**, **Đã hết hạn** và nhóm theo tháng hết hạn.

Hỗ trợ
------
NGUYEN VAN TINH - tinhnguyenvan91@gmail.com - 0909977920 - https://tweb.com.vn/
    """,
    "version": "17.0.1.1.0",
    "category": "Sales/Sales",
    "license": "LGPL-3",
    "author": "NGUYEN VAN TINH",
    "maintainer": "NGUYEN VAN TINH",
    "website": "https://tweb.com.vn/",
    "support": "tinhnguyenvan91@gmail.com",
    "depends": ["sale_management", "mail"],
    "data": [
        "data/mail_template_data.xml",
        "views/sale_order_views.xml",
    ],
    "images": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}

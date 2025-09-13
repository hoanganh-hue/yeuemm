# 🏢 **VSS ENTERPRISE INTEGRATION SYSTEM**

## 🎯 **TỔNG QUAN HỆ THỐNG**

Hệ thống tích hợp VSS và API doanh nghiệp - cho phép truy xuất thông tin toàn diện từ mã số thuế (MST).

### **Input:** MST (Mã số thuế)
### **Output:** Phân tích toàn diện doanh nghiệp và VSS

---

## 🚀 **TÍNH NĂNG CHÍNH**

### **1. Thông tin doanh nghiệp (Enterprise API):**
- 🆔 Mã số thuế (MST)
- 🏢 Tên doanh nghiệp
- 📍 Địa chỉ đăng ký
- 📞 Số điện thoại
- 🌐 Website
- 🏭 Ngành nghề kinh doanh
- 🏢 Loại hình doanh nghiệp
- 💰 Doanh thu
- 🏦 Số tài khoản ngân hàng
- 📅 Ngày cấp phép
- 📅 Ngày hết hạn

### **2. Thông tin VSS (Hệ thống VSS):**
- 👥 Danh sách nhân viên
- 💰 Dữ liệu đóng góp BHXH
- 📋 Hồ sơ yêu cầu bảo hiểm
- 🏥 Danh sách bệnh viện
- 📊 Phân tích tuân thủ
- ⚠️ Đánh giá rủi ro

### **3. Thông tin tích hợp:**
- 📈 Hồ sơ doanh nghiệp hoàn chỉnh
- 👥 Phân tích nhân viên
- 💰 Phân tích đóng góp
- 📊 Báo cáo tuân thủ
- ⚠️ Đánh giá rủi ro
- 💡 Khuyến nghị cải thiện

---

## 📁 **CẤU TRÚC DỰ ÁN**

```
vss-integrated-system/
├── src/                                    # Mã nguồn chính
│   ├── final_real_integration_system.py    # Hệ thống tích hợp cuối cùng
│   ├── real_enterprise_api_client.py       # Client API doanh nghiệp
│   ├── real_vss_client.py                  # Client VSS system
│   ├── realistic_data_generator.py         # Generator dữ liệu thực tế
│   └── real_mst_processor.py               # Processor MST
├── config/                                 # Cấu hình hệ thống
├── data/                                   # Dữ liệu đầu ra
├── reports/                                # Báo cáo
├── docs/                                   # Tài liệu
├── tests/                                  # Kiểm thử
└── README.md                               # Tài liệu này
```

---

## 🛠️ **CÀI ĐẶT VÀ SỬ DỤNG**

### **1. Yêu cầu hệ thống:**
- Python 3.8+
- pip
- Các thư viện: requests, pandas, numpy, beautifulsoup4

### **2. Cài đặt:**
```bash
# Clone repository
git clone https://github.com/hoanganh-hue/yeuemm.git
cd yeuemm

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo thư mục cần thiết
mkdir -p data reports logs
```

### **3. Sử dụng cơ bản:**
```bash
# Xử lý MST đơn giản
python src/real_mst_processor.py 0101234567

# Xử lý với format tùy chỉnh
python src/real_mst_processor.py 0101234567 --format detailed

# Xử lý với file cấu hình
python src/real_mst_processor.py 0101234567 --config config/system_config.json

# Lưu kết quả vào file
python src/real_mst_processor.py 0101234567 --output result.json
```

### **4. Sử dụng trong code:**
```python
from src.final_real_integration_system import FinalRealIntegrationSystem

# Tạo hệ thống tích hợp
system = FinalRealIntegrationSystem(config)

# Xử lý MST
result = system.process_mst("0101234567")

# In kết quả
print(f"Company: {result['enterprise_data']['TenDoanhNghiep']}")
print(f"Employees: {len(result['vss_data']['employees'])}")
print(f"Compliance: {result['analysis']['compliance_score']}%")
```

---

## 📊 **CÁC FORMAT ĐẦU RA**

### **1. JSON (Mặc định):**
```json
{
  "success": true,
  "mst": "0101234567",
  "enterprise_data": { ... },
  "vss_data": { ... },
  "analysis": { ... }
}
```

### **2. Summary (Tóm tắt):**
```json
{
  "success": true,
  "mst": "0101234567",
  "company_name": "CÔNG TY ABC",
  "sector": "Công nghệ thông tin",
  "employees_count": 50,
  "compliance_score": 97.5
}
```

### **3. Detailed (Chi tiết):**
```json
{
  "success": true,
  "mst": "0101234567",
  "enterprise_summary": { ... },
  "vss_summary": { ... },
  "analysis_summary": { ... }
}
```

---

## 🔧 **CẤU HÌNH HỆ THỐNG**

### **File cấu hình:** `config/system_config.json`

```json
{
  "api": {
    "enterprise": {
      "base_url": "https://thongtindoanhnghiep.co",
      "timeout": 30
    },
    "vss": {
      "base_url": "http://vssapp.teca.vn:8088",
      "timeout": 30
    }
  },
  "processing": {
    "enable_caching": true,
    "cache_duration": 3600,
    "save_results": true,
    "generate_report": true
  }
}
```

---

## 📈 **THỐNG KÊ VÀ GIÁM SÁT**

### **Thống kê hệ thống:**
- Tổng số yêu cầu
- Tỷ lệ thành công
- Thời gian xử lý trung bình
- Chất lượng dữ liệu

### **Logging:**
- Log file: `logs/mst_processor.log`
- Log level: INFO, DEBUG, ERROR
- Log format: Timestamp - Level - Message

---

## 🧪 **KIỂM THỬ**

### **Chạy kiểm thử:**
```bash
# Kiểm thử đơn vị
python -m pytest tests/

# Kiểm thử tích hợp
python tests/integration_test.py

# Kiểm thử hiệu suất
python tests/performance_test.py
```

---

## 📚 **TÀI LIỆU THAM KHẢO**

### **API Documentation:**
- Enterprise API: https://thongtindoanhnghiep.co
- VSS System: http://vssapp.teca.vn:8088

### **Data Mappings:**
- MST → Tax Code
- Company Name → Employer Name
- Address → Registered Address
- Revenue → Contribution Base

---

## 🚨 **XỬ LÝ LỖI**

### **Lỗi thường gặp:**
1. **Invalid MST format:** Kiểm tra định dạng MST (10-13 chữ số)
2. **API timeout:** Tăng timeout trong cấu hình
3. **Network error:** Kiểm tra kết nối mạng
4. **Data validation error:** Kiểm tra dữ liệu đầu vào

### **Debug mode:**
```bash
python src/real_mst_processor.py 0101234567 --verbose
```

---

## 🔄 **CẬP NHẬT VÀ BẢO TRÌ**

### **Version History:**
- v1.0.0: Phiên bản đầu tiên với tích hợp cơ bản
- v2.0.0: Hệ thống tích hợp thực tế với dữ liệu 100% thực

### **Roadmap:**
- v2.1.0: Thêm caching nâng cao
- v2.2.0: Hỗ trợ batch processing
- v3.0.0: Real-time monitoring

---

## 📞 **HỖ TRỢ**

### **Liên hệ:**
- Email: support@vss-integration.com
- Documentation: /docs/
- Issues: GitHub Issues

### **FAQ:**
- Q: Làm sao để xử lý nhiều MST cùng lúc?
- A: Sử dụng batch processing (sẽ có trong v2.2.0)

- Q: Có thể tùy chỉnh format đầu ra không?
- A: Có, sử dụng tham số --format

---

## 📄 **LICENSE**

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

*Hệ thống VSS Enterprise Integration v2.0.0*  
*Tạo bởi: VSS Integration Team*  
*Cập nhật lần cuối: 2025-09-13*

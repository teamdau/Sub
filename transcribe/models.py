from django.db import models
import uuid


class InputData(models.Model):
    # Sử dụng uuid làm khóa chính, tạo tự động bằng uuid4
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Trường lưu trữ văn bản do người dùng nhập
    input_text = models.TextField()  # Văn bản được nhập trực tiếp
    
    # Ngôn ngữ của transcript, với một số lựa chọn phổ biến
    language = models.CharField(
        max_length=20,
        choices=[
            ("en", "Anh"),
            ("ko", "Hàn Quốc"),
            ("vi", "Việt Nam"),
            ("es", "Tây Ban Nha"),
            ("fr", "Pháp"),
            ("de", "Đức"),
            ("ja", "Nhật Bản"),
            ("zh", "Trung Quốc"),
            ("ru", "Nga"),
            ("pt-BR", "Bồ Đào Nha (Brazil)"),
            ("pt-PT", "Bồ Đào Nha (Bồ Đào Nha)"),
        ],
        default="en",  # Ngôn ngữ mặc định là tiếng Anh
    )
    
    # Văn bản transcript được lưu sau khi xử lý
    transcript = models.TextField(default="")

    def __str__(self):
        # Phương thức trả về chuỗi đại diện cho object, bao gồm văn bản và ngôn ngữ
        return f"Text Data ({self.language})"

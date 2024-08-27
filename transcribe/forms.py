from django import forms
from .models import InputData
from django.core.validators import RegexValidator
import logging

# Set up logger
logger = logging.getLogger(__name__)


def time_str_to_seconds(time_str):
    try:
        parts = list(map(int, time_str.split(":")))
        if len(parts) == 3:
            hours, minutes, seconds = parts
        else:
            hours, minutes, seconds = 0, int(parts[0]), int(parts[1])
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, IndexError):
        return 0  # Trả về 0 nếu có lỗi với thời gian


class QueryForm(forms.ModelForm):
    class Meta:
        model = InputData
        fields = ("input_text", "language", "start_time", "end_time")  # Thay youtube_url bằng input_text
        widgets = {
            "input_text": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "placeholder": "Paste or type your text here...",
                    "rows": 10,
                }
            ),
        }

    start_time = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex="^(?:(?:\d:)?\d{1,2}:)\d{2}$",
                message="Enter valid timestamps (e.g., 00:00).",
                code="invalid_time",
            ),
        ],
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "00:00",
            }
        ),
    )

    end_time = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex="^(?:(?:\d:)?\d{1,2}:)\d{2}$",
                message="Enter valid timestamps (e.g., 00:00).",
                code="invalid_time",
            ),
        ],
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "00:00",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        input_text = cleaned_data.get("input_text")
        language = cleaned_data.get("language")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # Kiểm tra nếu văn bản nhập vào rỗng
        if not input_text:
            self.add_error("input_text", "This field cannot be empty.")
            return cleaned_data

        # Xử lý logic với văn bản thay vì với YouTube URL
        try:
            # Thực hiện các bước xử lý văn bản, ví dụ xử lý dấu câu, tách câu, tùy thuộc vào logic của bạn
            # Bạn có thể thêm logic xử lý ở đây, ví dụ: chuẩn hóa, kiểm tra văn bản theo ngôn ngữ

            # Kiểm tra thời gian nếu có nhập
            if start_time or end_time:
                # Nếu có transcript (hoặc text), xử lý logic thời gian
                max_time = len(input_text.split()) * 0.5  # Giả định 0.5s mỗi từ, tùy thuộc vào logic của bạn
                start_time_seconds = time_str_to_seconds(start_time) if start_time else 0
                end_time_seconds = time_str_to_seconds(end_time) if end_time else max_time

                if start_time_seconds > max_time or end_time_seconds > max_time:
                    self.add_error("start_time", "Enter a valid time range.")
                elif start_time_seconds > end_time_seconds:
                    self.add_error("start_time", "Start time cannot be greater than end time.")

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            self.add_error("input_text", "An error occurred while processing the text.")

        return cleaned_data

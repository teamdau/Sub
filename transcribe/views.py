from django.shortcuts import render, redirect
from .forms import QueryForm
from .models import InputData
from youtube_transcript_api.formatters import TextFormatter
from deepmultilingualpunctuation import PunctuationModel
import kss
import re
import uuid
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


def capitalize_sentences(text):
    sentence_pattern = r"(?:^|(?<=[.!?]))\s*(\w)"
    result = re.sub(sentence_pattern, lambda x: x.group(0).upper(), text)
    return result

def clean_text(text):
    # Loại bỏ các chuỗi như [Música]
    cleaned_text = re.sub(r'\[.*?\]', '', text)
    
    # Loại bỏ các dấu thời gian như (05:45)
    cleaned_text = re.sub(r'\(\d{2}:\d{2}\)', '', cleaned_text)
    
    # Xóa khoảng trắng thừa
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text

def text_to_paragraphs(text, max_sentences_per_paragraph=10, max_paragraph_length=300):
    sentence_delimiters = [".", "!", "?"]
    sentences = []
    current_sentence = ""
    paragraphs = []
    current_paragraph = ""
    paragraph_length = 0

    for char in text:
        current_sentence += char
        if char in sentence_delimiters:
            sentences.append(current_sentence)
            current_sentence = ""

    if current_sentence:
        sentences.append(current_sentence)

    for sentence in sentences:
        sentence = sentence.strip()  # Xóa khoảng trắng và xuống dòng
        if sentence:
            if current_paragraph:
                if (paragraph_length + len(sentence) + 1 <= max_paragraph_length) and (
                    len(current_paragraph.split(".")) < max_sentences_per_paragraph
                ):
                    current_paragraph += " "  # Thêm khoảng cách giữa các câu
                    current_paragraph += sentence
                    paragraph_length += len(sentence) + 1  # +1 cho khoảng cách
                else:
                    paragraphs.append(current_paragraph)
                    current_paragraph = sentence
                    paragraph_length = len(sentence)
            else:
                current_paragraph = sentence
                paragraph_length = len(sentence)

    if current_paragraph:
        paragraphs.append(current_paragraph)

    return paragraphs


def text_to_sentences(text):
    sentence_pattern = r"(?<=[.!?])\s+"
    sentences = re.split(sentence_pattern, text)
    return sentences


def process_transcript_by_language(language, cleaned_transcript):
    pm = PunctuationModel()
    if language == "en":
        cleaned_transcript = pm.restore_punctuation(cleaned_transcript)
        cleaned_transcript = re.sub(r"([?!~])\.", r"\1", cleaned_transcript)
        cleaned_transcript = capitalize_sentences(cleaned_transcript)
    elif language in ["ko", "ja"]:
        cleaned_transcript = ". ".join(kss.split_sentences(cleaned_transcript))
        cleaned_transcript = re.sub(r"([?!~])\.", r"\1", cleaned_transcript)
    elif language in ["es", "fr", "de", "pt-BR", "pt-PT", "ru"]:
        cleaned_transcript = pm.restore_punctuation(cleaned_transcript)
        cleaned_transcript = re.sub(r"([?!~])\.", r"\1", cleaned_transcript)
        cleaned_transcript = capitalize_sentences(cleaned_transcript)
    elif language == "zh":
        cleaned_transcript = pm.restore_punctuation(cleaned_transcript)
    
    return cleaned_transcript


def query_view(request):
    if request.method == "POST":
        form = QueryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.uid = uuid.uuid4()
            instance.transcript = form.cleaned_data.get("input_text")  # Lấy dữ liệu văn bản từ form
            instance.save()

            return redirect("transcribe", uid=instance.uid)
    else:
        form = QueryForm()
    return render(request, "index.html", {"form": form})


def transcribe(request, uid):
    try:
        data = InputData.objects.get(uid=uid)
    except InputData.DoesNotExist:
        return HttpResponseRedirect(reverse("query_view"))
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponseRedirect(reverse("query_view"))

    try:
        # Lấy dữ liệu từ model
        text = data.transcript
        language = data.language

        # Làm sạch văn bản bằng cách loại bỏ [Música] và (05:45)
        cleaned_text = clean_text(text)

        # Xử lý văn bản dựa trên ngôn ngữ
        processed_text = process_transcript_by_language(language, cleaned_text)

        # Chuyển transcript thành đoạn văn và câu
        paragraphs = text_to_paragraphs(processed_text)
        sentences = text_to_sentences(processed_text)

        # Render kết quả ra trang HTML
        return render(
            request,
            "transcribe/result.html",
            {
                "transcript": processed_text,
                "paragraphs": paragraphs,
                "sentences": sentences,
            },
        )

    except Exception as e:
        print(f"Error occurred during transcription: {e}")
        return HttpResponseRedirect(reverse("query_view"))


# import wave
# import json
# from vosk import Model, KaldiRecognizer

# # Tải mô hình Vosk (tải mô hình từ https://alphacephei.com/vosk/models và giải nén vào thư mục)
# model = Model("D:/vosk-model-cn-kaldi-multicn-0.15")

# # Mở tệp âm thanh
# wf = wave.open("file_1(mp3cut.net).wav", "rb")

# # Khởi tạo recognizer
# recognizer = KaldiRecognizer(model, wf.getframerate())

# # Đọc dữ liệu âm thanh và chuyển đổi thành văn bản
# results = []
# while True:
#     data = wf.readframes(4000)
#     if len(data) == 0:
#         break
#     if recognizer.AcceptWaveform(data):
#         result = recognizer.Result()
#         results.append(json.loads(result))

# # Kết quả cuối cùng
# final_result = recognizer.FinalResult()
# results.append(json.loads(final_result))

# # In ra văn bản chuyển đổi
# for result in results:
#     print(result.get("text", ""))
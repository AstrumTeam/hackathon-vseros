import cv2
import dlib
import sys
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip
from io import BytesIO

def process_video_file(input_file, smoothing_factor=0.1):
    """
    Обработка видео с обнаружением лиц и плавным центрированием, сохранением звука.
    
    :param input_file: Входной видеофайл как объект BytesIO.
    :param smoothing_factor: Параметр сглаживания движения камеры (по умолчанию 0.1).
    :return: Обработанное видео как объект BytesIO.
    """
    detector = dlib.get_frontal_face_detector()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(input_file.read())
        input_video_path = temp_input.name

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеофайл.")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    new_width = int(height * 9 / 16)
    new_height = height

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_output:
        output_video_path = temp_output.name

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (new_width, new_height))

    processed_frames = []

    center_x, center_y = width // 2, height // 2

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Обработка видео...")

    start_time = cv2.getTickCount()

    for frame_index in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print("Кадры закончились или ошибка при чтении кадра.")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_frame)

        if len(faces) > 0:
            face = faces[0]
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            new_center_x = x + w // 2
            new_center_y = y + h // 2
        else:
            new_center_x = width // 2
            new_center_y = height // 2

        center_x += (new_center_x - center_x) * smoothing_factor
        center_y += (new_center_y - center_y) * smoothing_factor

        start_x = max(int(center_x - new_width // 2), 0)
        start_y = max(int(center_y - new_height // 2), 0)

        start_x = min(start_x, width - new_width)
        start_y = min(start_y, height - new_height)

        cropped_frame = frame[start_y:start_y + new_height, start_x:start_x + new_width]
        processed_frames.append(cropped_frame)

        progress = (frame_index + 1) / total_frames
        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

        bar_length = 50
        block = int(bar_length * progress)
        progress_bar = f'\rОбработка: [{"#" * block + "-" * (bar_length - block)}] {progress * 100:.2f}% | Время: {elapsed_time:.2f} сек'
        sys.stdout.write(progress_bar)
        sys.stdout.flush()

    if processed_frames:
        for frame in processed_frames:
            out.write(frame)

        print("\nОбработка завершена. Видео сохранено.")
    else:
        print("Ошибка: Нет обработанных кадров для записи.")

    cap.release()
    out.release()

    # Добавление звука
    original_video = VideoFileClip(input_video_path)
    final_video = VideoFileClip(output_video_path).set_audio(original_video.audio)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_final_output:
        final_output_path = temp_final_output.name

    final_video.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

    final_video.close()
    original_video.close()

    with open(final_output_path, 'rb') as f:
        final_video_bytes = BytesIO(f.read())

    return final_video_bytes
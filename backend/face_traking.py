import cv2
import dlib
import sys
import numpy as np
import tempfile
from moviepy.editor import VideoFileClip, ImageSequenceClip
from io import BytesIO


def process_video_clip(video_clip, smoothing_factor=0.1):
    """
    Обработка видео с обнаружением лиц и плавным центрированием, сохранением звука.
    
    :param video_clip: Входной видеоклип как объект VideoFileClip.
    :param smoothing_factor: Параметр сглаживания движения камеры (по умолчанию 0.1).
    :return: Обработанный видеоклип как объект VideoFileClip.
    """
    detector = dlib.get_frontal_face_detector()

    fps = video_clip.fps
    width, height = video_clip.size

    new_width = int(height * 9 / 16)  # Новый размер с соотношением сторон 16:9
    new_height = height

    processed_frames = []

    center_x, center_y = width // 2, height // 2

    total_frames = int(video_clip.duration * fps)
    print("Обработка видео...")

    start_time = cv2.getTickCount()

    for frame_index, frame in enumerate(video_clip.iter_frames(fps=fps, dtype="uint8")):
        # Преобразуем кадр в оттенки серого для обнаружения лиц
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = detector(gray_frame)

        # Если лица найдены, используем первое для определения центра кадра
        if len(faces) > 0:
            face = faces[0]
            x, y, w, h = (face.left(), face.top(), face.width(), face.height())
            new_center_x = x + w // 2
            new_center_y = y + h // 2
        else:
            new_center_x = width // 2
            new_center_y = height // 2

        # Плавное перемещение центра кадра
        center_x += (new_center_x - center_x) * smoothing_factor
        center_y += (new_center_y - center_y) * smoothing_factor

        # Определяем начальные координаты для обрезки
        start_x = max(int(center_x - new_width // 2), 0)
        start_y = max(int(center_y - new_height // 2), 0)

        start_x = min(start_x, width - new_width)
        start_y = min(start_y, height - new_height)

        # Обрезаем кадр
        cropped_frame = frame[start_y:start_y + new_height, start_x:start_x + new_width]
        processed_frames.append(cropped_frame)

        # Выводим прогресс
        progress = (frame_index + 1) / total_frames
        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()

        bar_length = 50
        block = int(bar_length * progress)
        progress_bar = f'\rОбработка: [{"#" * block + "-" * (bar_length - block)}] {progress * 100:.2f}% | Время: {elapsed_time:.2f} сек'
        sys.stdout.write(progress_bar)
        sys.stdout.flush()

    if processed_frames:
        # Создаем новый видеоклип из обработанных кадров
        processed_clip = ImageSequenceClip(processed_frames, fps=fps)

        # Добавляем оригинальный звук обратно к обработанному клипу
        processed_clip = processed_clip.set_audio(video_clip.audio)
        
        print("\nОбработка завершена.")
        return processed_clip
    else:
        print("Ошибка: Нет обработанных кадров.")
        return None
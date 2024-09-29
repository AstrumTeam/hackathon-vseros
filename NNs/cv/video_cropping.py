from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip
import io
import os
import tempfile
from moviepy.video.VideoClip import VideoClip

def crop_video_to_9_16_test(video_clip):
    """
    Обрезает видео до соотношения сторон 9:16, центрируя его.
    Если разрешение меньше 1620x1080, изменяет размер до 576x1024.
    
    :param video_clip: Входной видеоклип (объект MoviePy VideoFileClip).
    :return: Обрезанный видеоклип (объект MoviePy VideoFileClip).
    """
    # Получаем ширину и высоту оригинального видео
    width, height = video_clip.size

    # Проверяем, если разрешение меньше 1620x1080
    if width < 1620 or height < 1080:
        # Изменяем размер до 576x1024
        resized_video = video_clip.resize(newsize=(576, 1024))
        return resized_video.set_audio(video_clip.audio)

    # Иначе, обрезаем до соотношения 9:16
    new_height = height
    new_width = int(new_height * 9 / 16)

    # Обрезаем видео по центру
    cropped_video = video_clip.crop(x_center=width / 2, y_center=height / 2, width=new_width, height=new_height)

    # Возвращаем обрезанный видеоклип
    return cropped_video.set_audio(video_clip.audio)

def crop_video_to_9_16(video_clip):
    """
    Обрезает видео до соотношения сторон 9:16, центрируя его, с учётом исходного соотношения пикселей.
    
    :param video_clip: Входной видеоклип (объект MoviePy VideoFileClip).
    :return: Обрезанный видеоклип (объект MoviePy VideoFileClip).
    """
    # Получаем ширину и высоту оригинального видео
    width, height = video_clip.size

    # Рассчитываем фактическое соотношение сторон
    aspect_ratio = width / height

    print(aspect_ratio)

    # Рассчитываем желаемую высоту и ширину для 9:16
    new_height = height
    new_width = int(new_height * 9 / 16)

    # Проверка, если рассчитанная ширина превышает оригинальную ширину
    if new_width > width:
        # Если да, то пересчитываем высоту
        new_width = width
        new_height = int(new_width * 16 / 9)

    # Теперь мы знаем, что new_width и new_height соответствуют соотношению 9:16
    # Обрезаем видео по центру
    cropped_video = video_clip.crop(x_center=width / 2, y_center=height / 2, width=new_width, height=new_height)

    # Возвращаем обрезанный видеоклип
    return cropped_video

def crop_video_to_9_16_with_fields(video_clip):
    """
    Масштабирует видео до ширины 720px и добавляет черные поля для сохранения соотношения 9:16.
    
    :param video_clip: Входной видеоклип (объект MoviePy VideoFileClip).
    :return: Обработанный видеоклип с полями (объект MoviePy VideoFileClip).
    """
    # Размеры целевого видео 9:16
    target_width = 720
    target_height = 1280

    # Масштабируем видео до целевой ширины
    resized_video = video_clip.resize(width=target_width)

    # Если высота превышает 1280, обрезаем
    if resized_video.size[1] > target_height:
        crop_y = (resized_video.size[1] - target_height) / 2
        resized_video = resized_video.crop(y1=crop_y, y2=crop_y + target_height)

    # Создаем черный фон для 9:16
    black_bars = ColorClip(size=(target_width, target_height), color=(0, 0, 0)).set_duration(video_clip.duration)

    # Центрируем видео на фоне
    final_video = CompositeVideoClip([black_bars, resized_video.set_position("center")])

    # Возвращаем обработанный видеоклип
    return final_video
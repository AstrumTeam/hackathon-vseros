from io import BytesIO
from face_traking_module import process_video_clip
from scene_detection_module import detect_scenes
import os
from video_cropping import crop_video_to_9_16, crop_video_to_9_16_with_fields
import moviepy.editor as mp

input_video_path = "/Users/vladislav/Временное/musk_cutted.mp4"  # Укажите путь к вашему видео
output_video_path = "/Users/vladislav/Временное/output_video.mp4"  # Путь для сохранения обработанного видео

# #С ТРЕКИНГОМ
# if __name__ == "__main__":
#     # Чтение входного видео
#     video_path = "/Users/vladislav/Временное/gavrilina.mp4"
#     print(f"Reading input video from: {video_path}")

#     with open(video_path, "rb") as f:
#         input_video = BytesIO(f.read())

#     # Вызов функции
#     output_video = process_video_file(input_video)

#     # Определяем путь для сохранения выходного видео
#     output_path = os.path.join(os.path.dirname(video_path), "output_video_gavrilina_traking.mp4")
    
#     # Сохранение выходного видео в той же папке
#     with open(output_path, "wb") as f:
#         f.write(output_video.getbuffer())
    
#     print(f"Output video saved to: {output_path}")


# with open('/Users/vladislav/Временное/musk.mp4', 'rb') as f:
#     input_video_bytes = BytesIO(f.read())

# scene_timestamps = detect_scenes(input_video_bytes)

# for i, (start, end) in enumerate(scene_timestamps):
#     print(f"Сцена {i + 1}: {start} - {end}")





# # #БЕЗ ТРЕКИНГА
# if __name__ == "__main__":
#     # Чтение входного видео
#     video_path = "/Users/vladislav/Временное/gavrilina.mp4"
#     print(f"Reading input video from: {video_path}")

#     with open(video_path, "rb") as f:
#         input_video = BytesIO(f.read())

#     # Вызов функции
#     output_video = crop_video_to_9_16(input_video)

#     # Определяем путь для сохранения выходного видео
#     output_path = os.path.join(os.path.dirname(video_path), "output_video_gavrilina.mp4")
    
#     # Сохранение выходного видео в той же папке
#     with open(output_path, "wb") as f:
#         f.write(output_video.getbuffer())
    
#     print(f"Output video saved to: {output_path}")


# # БЕЗ ТРЕКИНГА С ПОЛЯМИ
# if __name__ == "__main__":
#     # Чтение входного видео
#     video_path = "/Users/vladislav/Временное/gavrilina.mp4"
#     print(f"Reading input video from: {video_path}")

#     with open(video_path, "rb") as f:
#         input_video = BytesIO(f.read())

#     # Вызов функции
#     output_video = crop_video_to_9_16_with_fields(input_video)

#     # Определяем путь для сохранения выходного видео
#     output_path = os.path.join(os.path.dirname(video_path), "output_video_gavrilina_fields.mp4")
    
#     # Сохранение выходного видео в той же папке
#     with open(output_path, "wb") as f:
#         f.write(output_video.getbuffer())
    
#     print(f"Output video saved to: {output_path}")

# Загружаем исходное видео


#ТРЭКИНГ MoviePy
# try:
#     # Чтение видео с помощью MoviePy
#     video_clip = mp.VideoFileClip(input_video_path)

#     # Обработка видео
#     processed_clip = process_video_clip(video_clip)

#     if processed_clip:
#         # Сохранение обработанного видео в файл
#         processed_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
#         print(f"Обработанное видео сохранено в {output_video_path}")
#     else:
#         print("Ошибка при обработке видео.")
# except Exception as e:
#     print(f"Произошла ошибка: {e}")

try:
    # Чтение видео с помощью MoviePy
    video_clip = mp.VideoFileClip(input_video_path)

    # Обработка видео
    processed_clip = crop_video_to_9_16_with_fields(video_clip)

    if processed_clip:
        # Сохранение обработанного видео в файл
        processed_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
        print(f"Обработанное видео сохранено в {output_video_path}")
    else:
        print("Ошибка при обработке видео.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
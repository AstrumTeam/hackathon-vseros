import moviepy.editor as mp
import numpy as np
import librosa
import matplotlib.pyplot as plt

# 1. Извлечем аудиодорожку из видео
def extract_audio_from_video(video_path, audio_output):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output)
    return audio_output

# 2. Анализ аудиодорожки
def analyze_audio(audio_path, sr=22050):
    # Загружаем аудиофайл
    audio, sample_rate = librosa.load(audio_path, sr=sr)
    
    # 3. Извлекаем интенсивность (амплитуду) звука
    intensity = librosa.feature.rms(audio)[0]
    
    # 4. Находим моменты резкого изменения интенсивности
    peaks = np.where(intensity > np.percentile(intensity, 90))[0]
    
    # Преобразуем в секунды
    peak_times = librosa.frames_to_time(peaks, sr=sample_rate)
    
    return peak_times, intensity

# 5. Выводим график интенсивности
def plot_intensity(intensity, sr=22050):
    plt.figure(figsize=(14, 5))
    times = librosa.frames_to_time(np.arange(len(intensity)), sr=sr)
    plt.plot(times, intensity)
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity')
    plt.title('Audio Intensity Over Time')
    plt.show()

# Пример использования
video_path = 'your_video.mp4'
audio_output = 'audio.wav'

# 1. Извлекаем аудио из видео
audio_path = extract_audio_from_video(video_path, audio_output)

# 2. Анализируем аудиодорожку
peak_times, intensity = analyze_audio(audio_path)

# 3. Выводим тайм-коды ярких моментов
print("Тайм-коды ярких моментов: ", peak_times)

# 4. Отрисовываем график интенсивности звука
plot_intensity(intensity)
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})

def add_subtitles_to_clip(clip, subtitles):
    """
    Метод для добавления субтитров на видео клип.
    
    Аргументы:
    clip - объект MoviePy VideoFileClip
    subtitles - массив словарей, где каждый словарь содержит:
        - "start": время старта субтитров в секундах
        - "end": время окончания субтитров в секундах
        - "text": текст субтитра
    
    Возвращает:
    Новый клип с наложенными субтитрами внизу.
    """
    absolute_start = subtitles[0]['start']
    
    # Создаем список клипов для субтитров
    subtitle_clips = []
    
    for subtitle in subtitles:
        start = subtitle['start'] - absolute_start
        end = subtitle['end'] - absolute_start
        text = subtitle['text']

        rgb_color = (209, 183, 53)  # Красный
        hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_color)


        # new_text = '\n'.join(text[i:i+24] for i in range(0, len(text), 24))

        
        # Создаем текстовый клип для каждого субтитра
        subtitle_clip = TextClip(
            text, fontsize=25, color=hex_color, font='DejaVu-Sans-Mono', 
            bg_color='transparent', size=(clip.w, 100), stroke_color=hex_color, 
            stroke_width=2, method='caption', align='center', kerning=-1
        ).set_duration(end - start).set_start(start)
        
        # Позиционируем субтитры внизу видео с отступом
        subtitle_clip = subtitle_clip.set_position(('center', clip.h - 60))  # 'bottom' с отступом 60 пикселей
        
        # Добавляем текстовый клип в общий список
        subtitle_clips.append(subtitle_clip)
    
    # Создаем композитное видео с наложенными субтитрами
    final_clip = CompositeVideoClip([clip] + subtitle_clips)
    
    return final_clip
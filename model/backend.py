from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, effects
import csv
import stable_whisper

from clf_model import InterestClassificationModel
from processing import Processing
import os

class Backend:
    def __init__(self):
        self.__clf_model = InterestClassificationModel()
        self.__processing = Processing()


        self.__model_whisper = stable_whisper.load_model('tiny')
        self.__audio_file_name = "out_audio"
        self.__model_whisper_out_name = 'audio.tsv'


    def work(self, upload_file):
        # self.__get_audio(upload_file)
        # model_whisper_out = self.__model_whisper.transcribe(f'{self.__audio_file_name}.mp3')
        # model_whisper_out.to_tsv(self.__model_whisper_out_name)
        # self.__clear_files()

        interest_tags = []
        current_index = 0
        tags = self.__processing_transcribe(self.__model_whisper_out_name)
        while current_index < len(tags)-5:
            start_index = current_index
            # end_index = len(self.__cut_tags(tags[start_index]['start'], tags[start_index]['start']+10, tags)) + current_index
            end_index = start_index+5

            clip_text = ''.join([x['text']+' ' for x in tags[start_index:end_index]])
            clip_sentences = self.__processing.split_by_sentences(clip_text)

        clip = VideoFileClip(upload_file)
        clip = clip.subclip(0, 10)
        clip.write_videofile(f'new_{upload_file}')

    
    def __cut_tags(self, start, end, subtitles):
        return list(filter(lambda x: start<=x['start'] and x['start'] <= end, subtitles))  

    def __processing_transcribe(self, file):
        tags = []
        tsv_file = open(file)

        read_tsv = csv.reader(tsv_file, delimiter="\t")
        for row in read_tsv:
            if len(row) > 0:
                tags.append({
                    "start": int(row[0]) / 1000,
                    "end": int(row[1]) / 1000,
                    "text": row[-1]
                })
        return tags
    

    def __get_audio(self, file):
        audioclip = AudioFileClip(file)
        audioclip.write_audiofile(f'{self.__audio_file_name}.wav')

        norm_sound = AudioSegment.from_file(f'{self.__audio_file_name}.wav', format='wav')
        norm_sound = effects.normalize(norm_sound)
        norm_sound.export(f'{self.__audio_file_name}.mp3', format='mp3')


    def __clear_files(self):
        os.remove(f'{self.__audio_file_name}.mp3')
        os.remove(f'{self.__audio_file_name}.wav')
        # os.remove('audio.tsv')

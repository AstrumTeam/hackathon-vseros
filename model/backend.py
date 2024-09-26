from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, effects
import csv
import stable_whisper

from models import InterestClassificationModel
from processing import Processing
import os

class Backend:
    def __init__(self):
        self.__clf_interest_model = InterestClassificationModel()
        self.__processing = Processing()


        self.__model_whisper = stable_whisper.load_model('tiny')
        self.__audio_file_name = "out_audio"
        self.__model_whisper_out_name = 'transcribe_audio'


    def work(self, upload_file, threshold=0.5):
        # self.__get_audio(upload_file)
        # model_whisper_out = self.__model_whisper.transcribe(f'{self.__audio_file_name}.mp3')
        # model_whisper_out.to_tsv(f'{self.__model_whisper_out_name}.tsv')
        # self.__clear_files()

        tags = self.__processing_transcribe(f'{self.__model_whisper_out_name}.tsv')
        sentences_tags = self.__split_tags_by_sentences(tags)
        sentences = [x['text'] for x in sentences_tags]
        return sentences
    
        # sentences_interest = self.__clf_interest_model.predict(sentences)
        # return sentences_interest

        # clip = VideoFileClip(upload_file)
        # clip = clip.subclip(0, 10)
        # clip.write_videofile(f'new_{upload_file}')


    def __get_audio(self, file):
        audioclip = AudioFileClip(file)
        audioclip.write_audiofile(f'{self.__audio_file_name}.wav')

        norm_sound = AudioSegment.from_file(f'{self.__audio_file_name}.wav', format='wav')
        norm_sound = effects.normalize(norm_sound)
        norm_sound.export(f'{self.__audio_file_name}.mp3', format='mp3')


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
    
    def __split_tags_by_sentences(self, tags):
        sentences_tags = []
        current_index = 0
        while current_index <= len(tags)-2:
            start, end = current_index, current_index+1

            clip_text = tags[start]['text']
            count_sentences = len(self.__processing.split_by_sentences(clip_text))

            stop_flag = False
            while stop_flag == False:
                new_clip_text = ''.join([x['text']+' ' for x in tags[start:end+1]])
                new_count_sentences = len(self.__processing.split_by_sentences(new_clip_text))

                if new_count_sentences != count_sentences:
                    current_index = end
                    sentence_tag = {'start': tags[start]['start'], 'end': tags[end-1]['end'], 'text': clip_text}
                    sentences_tags.append(sentence_tag)
                    stop_flag = True
                else:
                    clip_text = new_clip_text
                    end += 1
        return sentences_tags


    def __clear_files(self):
        os.remove(f'{self.__audio_file_name}.mp3')
        os.remove(f'{self.__audio_file_name}.wav')
        os.remove(f'{self.__model_whisper_out_name}.tsv')

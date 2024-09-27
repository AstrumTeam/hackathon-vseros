from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, effects
import csv
import stable_whisper
from scipy.ndimage.filters import gaussian_filter
from sklearn.preprocessing import minmax_scale

from models import InterestClassificationModel
from processing import Processing
import os

class Backend:
    def __init__(self):
        print('1')
        self.__clf_interest_model = InterestClassificationModel()
        print('2')
        self.__processing = Processing()
        print('3')


        self.__model_whisper = stable_whisper.load_model('large-v3') #large-v3
        print('4')
        self.__audio_file_name = "out_audio"
        self.__model_whisper_out_name = 'transcribe_audio'

    def work(self, upload_filename, 
             threshold = 0.5, min_length = 10, max_length = 60, 
             subtitles = False, fields = False, face_tracking = False,
             humor = False, clickbait = False):
        
        self.__get_audio(upload_filename)
        model_whisper_out = self.__model_whisper.transcribe("videos/" + f'{self.__audio_file_name}.mp3')
        model_whisper_out.to_tsv("videos/" + f'{self.__model_whisper_out_name}.tsv')

        tags = self.__processing_transcribe(f'{self.__model_whisper_out_name}.tsv')
        sentences_tags = self.__split_tags_by_sentences(tags)

        sentences = [x['text'] for x in sentences_tags]
        sentences_interest = self.__clf_interest_model.predict(sentences)

        interest_tags =  self.__normalize(sentences_interest, threshold)

        clip_tags = []
        current_index = 0
        while current_index <= len(interest_tags)-1:
            if interest_tags[current_index] == 1:
                start_index = current_index
                end_index = current_index+1
                if interest_tags[end_index] == 1:
                    while interest_tags[end_index+1] == 1:
                        end_index = end_index+1

                    time_start = sentences_tags[start_index]['start']
                    time_end = sentences_tags[end_index]['end']

                    if time_end - time_start >= min_length and time_end - time_start <= max_length:
                        clip = {'start': time_start, 'end': time_end, 'subtitles': sentences_tags[start_index:end_index+1]}
                        clip_tags.append(clip)
                current_index = end_index+1
            else:
                current_index +=1

        clip_names= []
        video = VideoFileClip("videos/" + upload_filename)
        for i in range(len(clip_tags)):
            clip = video.subclip(clip_tags[i]['start'], clip_tags[i]['end'])

            upload_name = upload_filename.split('.')[0]
            clip_name = f'videos/{upload_name}_{i}.mp4'
            clip.write_videofile(clip_name, fps=30, threads=1, codec="libx264", audio=True, audio_codec="aac")
            clip_names.append(clip_name)
        
        return clip_names


    def __get_audio(self, file):
        audioclip = AudioFileClip("videos/" + file)
        audioclip.write_audiofile("videos/" + f'{self.__audio_file_name}.wav')

        norm_sound = AudioSegment.from_file("videos/" + f'{self.__audio_file_name}.wav', format='wav')
        norm_sound = effects.normalize(norm_sound)
        norm_sound.export("videos/" + f'{self.__audio_file_name}.mp3', format='mp3')


    def __processing_transcribe(self, file):
        tags = []
        tsv_file = open("videos/" + file)

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
    
    def __normalize(self, pred, threshold=0.5):
        pred_soft = []
        pred_soft = pred_soft + pred[:3]
        for i in range(3, len(pred)-3):
            new_i = (pred[i-3] + pred[i-2] + pred[i-1] + pred[i] + pred[i+1] + pred[i+2] + pred[i+3])/9
            pred_soft.append(new_i)
        pred_soft = pred_soft + pred[-4:]
            
        soft = gaussian_filter(pred_soft, sigma=.8)
        soft_min_max = minmax_scale(soft, feature_range=(0,1))

        result = []
        for tag in soft_min_max:
            if tag >= threshold:
                result.append(1)
            else:
                result.append(0)
        return result

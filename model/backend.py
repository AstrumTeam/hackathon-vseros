import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment, effects
import csv
import stable_whisper
from scipy.ndimage.filters import gaussian_filter
from sklearn.preprocessing import minmax_scale
import shutil
import uuid

from models import InterestClassificationModel
from processing import Processing
from video_cropping import crop_video_to_9_16, crop_video_to_9_16_with_fields
from face_traking import process_video_clip
from subtitles import add_subtitles_to_clip

class Backend:
    def __init__(self):
        self.__clf_interest_model = InterestClassificationModel()
        self.__processing = Processing()


        self.__model_whisper = stable_whisper.load_model('large-v2') #large-v3
        self.__audio_file_name = "out_audio"
        self.__model_whisper_out_name = 'transcribe_audio'

    def work(self, upload_filename, 
             threshold = 0.5, min_length = 10, max_length = 61800, 
             subtitles = False, fields = True, face_tracking = False,
             humor = False, clickbait = False):
        
        self.__get_audio(upload_filename)
        model_whisper_out = self.__model_whisper.transcribe("videos/" + f'{self.__audio_file_name}.mp3')
        model_whisper_out.to_tsv("videos/" + f'{self.__model_whisper_out_name}.tsv')

        print('processing_transcribe')
        tags = self.__processing_transcribe(f'{self.__model_whisper_out_name}.tsv')
        print(len(tags))

        print('split_tags_by_sentences')
        sentences_tags = self.__split_tags_by_sentences(tags)
        print(len(sentences_tags))
        print(sentences_tags)


        video = VideoFileClip("videos/" + upload_filename)


        print('get_interest_clip_tags')
        interest_clip_tags = self.__get_interest_clip_tags(sentences_tags=tags, threshold=threshold, min_length=min_length, max_length=max_length)
        print(len(interest_clip_tags))

        interest_clip_names= []
        print('interest_clips')
        for i in range(len(interest_clip_tags)):
            clip = video.subclip(interest_clip_tags[i]['start'], interest_clip_tags[i]['end'])


            if face_tracking == True:
                clip = process_video_clip(clip)
            else:
                if fields == True:
                    clip = crop_video_to_9_16_with_fields(clip)
                else:
                    clip = crop_video_to_9_16(clip)
            
            if subtitles:
                clip = add_subtitles_to_clip(clip, interest_clip_tags[i]['subtitles'])

            clip_name = str(uuid.uuid4())
            clip.write_videofile('results/' + clip_name + '.mp4', fps=30, threads=1, codec="libx264", audio=True, audio_codec="aac")
            interest_clip_names.append(clip_name)



        humor_clip_names = []
        if humor:
            print('get_humor_clip_tags')
            humor_clip_tags = self.__get_humor_clip_tags(sentences_tags=tags, threshold=threshold, min_length=min_length, max_length=max_length)
            print(len(humor_clip_tags))
            
            print('humor_clips')
            for i in range(len(humor_clip_tags)):
                clip = video.subclip(humor_clip_tags[i]['start'], humor_clip_tags[i]['end'])


                if face_tracking == True:
                    clip = process_video_clip(clip)
                else:
                    if fields == True:
                        clip = crop_video_to_9_16_with_fields(clip)
                    else:
                        clip = crop_video_to_9_16(clip)
                
                if subtitles:
                    clip = add_subtitles_to_clip(clip, humor_clip_tags[i]['subtitles'])

                clip_name = str(uuid.uuid4())
                clip.write_videofile('results/' + clip_name + '.mp4', fps=30, threads=1, codec="libx264", audio=True, audio_codec="aac")
                humor_clip_names.append(clip_name)



        clickbait_clip_names = []
        if clickbait:
            print('get_clickbait_clip_tags')
            clickbait_clip_tags = self.__get_clickbait_clip_tags(sentences_tags=tags, threshold=threshold, min_length=min_length, max_length=max_length)
            print(len(clickbait_clip_tags))

            print('clickbait_clips')
            for i in range(len(clickbait_clip_tags)):
                clip = video.subclip(clickbait_clip_tags[i]['start'], clickbait_clip_tags[i]['end'])


                if face_tracking == True:
                    clip = process_video_clip(clip)
                else:
                    if fields == True:
                        clip = crop_video_to_9_16_with_fields(clip)
                    else:
                        clip = crop_video_to_9_16(clip)
                
                if subtitles:
                    clip = add_subtitles_to_clip(clip, clickbait_clip_tags[i]['subtitles'])

                clip_name = str(uuid.uuid4())
                clip.write_videofile('results/' + clip_name + '.mp4', fps=30, threads=1, codec="libx264", audio=True, audio_codec="aac")
                clickbait_clip_names.append(clip_name)

        all_clips = []
        for clip in interest_clip_names:
            all_clips.append([clip, 'interest', 10])

        for clip in humor_clip_names:
            all_clips.append([clip, 'humor', 10])

        for clip in clickbait_clip_names:
            all_clips.append([clip, 'clickbait', 10])
        
        self.__clear()
        return all_clips
    
    
    
    def __get_interest_clip_tags(self, sentences_tags, threshold, min_length, max_length):
        sentences = [x['text'] for x in sentences_tags]
        sentences_interest = self.__clf_interest_model.predict(sentences)

        interest_tags =  self.__normalize(sentences_interest, threshold)

        clip_tags = []
        current_index = 0
        while current_index < len(interest_tags)-2:
            if interest_tags[current_index] == 1:
                start_index = current_index
                end_index = current_index+1
                if interest_tags[end_index] == 1:
                    while interest_tags[end_index+1] == 1 and end_index+1 != len(interest_tags)-1:
                        end_index = end_index+1

                    time_start = sentences_tags[start_index]['start']
                    time_end = sentences_tags[end_index]['end']

                    if time_end - time_start >= min_length and time_end - time_start <= max_length:
                        clip = {'start': time_start, 'end': time_end, 'subtitles': sentences_tags[start_index:end_index+1]}
                        clip_tags.append(clip)
                current_index = end_index+1
            else:
                current_index +=1

        return clip_tags
    
    
    def __get_humor_clip_tags(self, sentences_tags, threshold, min_length, max_length):
        sentences = [x['text'] for x in sentences_tags]
        sentences_interest = self.__clf_interest_model.predict(sentences)
        print()

        interest_tags =  self.__normalize(sentences_interest, threshold)

        clip_tags = []
        current_index = 0
        while current_index < len(interest_tags)-2:
            if interest_tags[current_index] == 1:
                start_index = current_index
                end_index = current_index+1
                if interest_tags[end_index] == 1:
                    while interest_tags[end_index+1] == 1 and end_index+1 != len(interest_tags)-1:
                        end_index = end_index+1

                    time_start = sentences_tags[start_index]['start']
                    time_end = sentences_tags[end_index]['end']

                    if time_end - time_start >= min_length and time_end - time_start <= max_length:
                        clip = {'start': time_start, 'end': time_end, 'subtitles': sentences_tags[start_index:end_index+1]}
                        clip_tags.append(clip)
                current_index = end_index+1
            else:
                current_index +=1

        return clip_tags

    
    
    def __get_clickbait_clip_tags(self, sentences_tags, threshold, min_length, max_length):
        sentences = [x['text'] for x in sentences_tags]
        sentences_interest = self.__clf_interest_model.predict(sentences)
        print()

        interest_tags =  self.__normalize(sentences_interest, threshold)

        clip_tags = []
        current_index = 0
        while current_index < len(interest_tags)-2:
            if interest_tags[current_index] == 1:
                start_index = current_index
                end_index = current_index+1
                if interest_tags[end_index] == 1:
                    while interest_tags[end_index+1] == 1 and end_index+1 != len(interest_tags)-1:
                        end_index = end_index+1

                    time_start = sentences_tags[start_index]['start']
                    time_end = sentences_tags[end_index]['end']

                    if time_end - time_start >= min_length and time_end - time_start <= max_length:
                        clip = {'start': time_start, 'end': time_end, 'subtitles': sentences_tags[start_index:end_index+1]}
                        clip_tags.append(clip)
                current_index = end_index+1
            else:
                current_index +=1

        return clip_tags


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
        all_text = ' '.join([x['text'] for x in tags])
        sentences_tags = []
        if (len(self.__processing.split_by_sentences(all_text)) < 20):
            current_index = 0
            while current_index < len(tags)-4:
                start, end = current_index, current_index+2
                clip_text = ' '.join([x['text'] for x in tags[start:end+1]])
                sentence_tag = {'start': tags[start]['start'], 'end': tags[end]['end'], 'text': clip_text}
                sentences_tags.append(sentence_tag)
                current_index = end+1
        else:
            print(1)
            current_index = 0
            while current_index < len(tags)-3:
                print(str(current_index) + ' 2')
                start, end = current_index, current_index+1

                clip_text = tags[start]['text']
                count_sentences = len(self.__processing.split_by_sentences(clip_text))

                stop_flag = False
                while stop_flag == False or end != len(tags)-1:
                    print(str(current_index) + ' 3')
                    new_clip_text = ' '.join([x['text'] for x in tags[start:end+1]])
                    new_count_sentences = len(self.__processing.split_by_sentences(new_clip_text))

                    if new_count_sentences != count_sentences:
                        print(str(current_index) + ' 4')
                        current_index = end
                        sentence_tag = {'start': tags[start]['start'], 'end': tags[end-1]['end'], 'text': clip_text}
                        sentences_tags.append(sentence_tag)
                        stop_flag = True
                    else:
                        print(str(current_index) + ' 5')
                        clip_text = new_clip_text
                        end += 1
        return sentences_tags
    
    def __normalize(self, pred, threshold=0.5):
        pred_soft = []
        pred_soft = pred_soft + pred[:4]
        for i in range(4, len(pred)-4):
            new_i = (pred[i-4] + pred[i-3] + pred[i-2] + pred[i-1] + pred[i] + pred[i+1] + pred[i+2] + pred[i+3] + pred[i+4])/9
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
    
    def __clear(self):
        if os.path.exists("videos"):
            try:
                shutil.rmtree("videos")
            except Exception as e:
                print("/videos not deleted")
from io import BytesIO
from face_traking_module import process_video_file
from scene_detection_module import detect_scenes

# with open('NNs/enina2.mp4', 'rb') as f:
#     input_video_bytes = BytesIO(f.read())
# processed_video_bytes = process_video_file(input_video_bytes)
# with open('processed_video.mp4', 'wb') as f:
#     f.write(processed_video_bytes.getvalue())

with open('/Users/vladislav/Временное/musk.mp4', 'rb') as f:
    input_video_bytes = BytesIO(f.read())

scene_timestamps = detect_scenes(input_video_bytes)

for i, (start, end) in enumerate(scene_timestamps):
    print(f"Сцена {i + 1}: {start} - {end}")
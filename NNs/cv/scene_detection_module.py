from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from io import BytesIO
import tempfile

def detect_scenes(input_video: BytesIO):
    """
    Обнаружение сцен в видео, переданном в виде объекта BytesIO.

    :param input_video: Видео как объект BytesIO.
    :return: Список таймкодов начала и конца каждой сцены.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(input_video.read())
        temp_video_path = temp_video.name

    video_manager = VideoManager([temp_video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list()

    video_manager.release()

    return [(start.get_timecode(), end.get_timecode()) for start, end in scene_list]
import unittest
import os
from Merge import merge_video_audio_subs, cleanup_temp_files

class MergeTester(unittest.TestCase):

    def setUp(self):
        self.video_mp4 = os.path.join("PyCutieMerge/src/test_files", "video.mp4")
        self.video_webm = os.path.join("PyCutieMerge/src/test_files", "video.webm")
        self.audio_opus = os.path.join("PyCutieMerge/src/test_files", "audio.opus")
        self.subs_ass = os.path.join("PyCutieMerge/src/test_files", "subs.ass")
        self.output_dir = "PyCutieMerge/src/test_files"
        os.makedirs(self.output_dir, exist_ok=True)

    def test_merge_mp4_opus_no_subs(self):
        output_file = os.path.join(self.output_dir, "mp4_opus_no_subs.mkv")
        result = merge_video_audio_subs(self.video_mp4, self.audio_opus, output_filename=output_file)
        self.assertTrue(result, "Объединение mp4+opus без субтитров не удалось")
        self.assertTrue(os.path.exists(output_file), "Файл не создан")

    def test_merge_mp4_opus_with_subs(self):
        output_file = os.path.join(self.output_dir, "mp4_opus_with_subs.mkv")
        result = merge_video_audio_subs(self.video_mp4, self.audio_opus, self.subs_ass, output_filename=output_file)
        self.assertTrue(result, "Объединение mp4+opus с субтитрами не удалось")
        self.assertTrue(os.path.exists(output_file), "Файл не создан")

    def test_merge_webm_opus_no_subs(self):
        output_file = os.path.join(self.output_dir, "webm_opus_no_subs.mkv")
        result = merge_video_audio_subs(self.video_webm, self.audio_opus, output_filename=output_file)
        self.assertTrue(result, "Объединение webm+opus без субтитров не удалось")
        self.assertTrue(os.path.exists(output_file), "Файл не создан")

    def test_merge_webm_opus_with_subs(self):
        output_file = os.path.join(self.output_dir, "webm_opus_with_subs.mkv")
        result = merge_video_audio_subs(self.video_webm, self.audio_opus, self.subs_ass, output_filename=output_file)
        self.assertTrue(result, "Объединение webm+opus с субтитрами не удалось")
        self.assertTrue(os.path.exists(output_file), "Файл не создан")

    # Удаление временных файлов
    # def tearDown(self):
    #     # cleanup_temp_files()

if __name__ == '__main__':
    unittest.main()
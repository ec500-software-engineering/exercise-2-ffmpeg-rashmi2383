import os
import subprocess
from main import encode_file


class BasicEncodeTest(Object):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode_function_should_create_new_file(self):
        encode_file(
            'mov.avi',
            'mov.mp4',
            '1',
            '30',
            '480'
        )
        assert os.path.exists('mov.mp4')

    def get_video_length(self, filename):
        raw_output = subprocess.check_output(
            ['ffprobe', filename],
            stderr=subprocess.STDOUT
        ).decode('utf-8')
        output_lines = str(raw_output).split('\n')
        for line in output_lines:
            if 'Duration' in line:
                return line.lstrip().split(' ')[1].split('.')[0]

    def test_output_video_duration_should_match_input_duration(self):
        encode_file(
            'mov.avi',
            'mov.mp4',
            '1',
            '30',
            '480'
        )
        length1 = self.get_video_length('mov.avi')
        length2 = self.get_video_length('mov1.mp4')
        assert length1 == length2

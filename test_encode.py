import os
import json
import pytest
import subprocess
from main import encode_file


@pytest.fixture(scope='session')
def video_path(tmpdir_factory):
    output_path = tmpdir_factory.mktemp(
        'media'
    ).join('mov.avi')
    cmd = 'ffmpeg -f lavfi -i smptebars -t 10 {}'.format(
        str(output_path)
    )
    subprocess.check_call(
        cmd.split(' ')
    )
    return output_path


class Test(object):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode_function_should_create_new_file(self, video_path):
        output_path = os.path.join(
            os.path.dirname(
                os.path.realpath(video_path)
            ),
            'mov.mp4'
        )
        encode_file(
            video_path,
            output_path,
            '1',
            '30',
            '480'
        )
    assert os.path.exists('video_path')

    def get_video_length(self, filename):
        proc_out = subprocess.Popen(
            ['ffprobe', '-print_format', 'json',
             '-show_format', '-show_streams', filename],
            stderr=subprocess.DEVNULL,
            stdout=subprocess.PIPE
        )
        json_raw = ''
        for line in proc_out.stdout.readlines():
            json_raw += line.decode('utf-8')
        json_data = json.loads(json_raw)
        duration = int(round(float(json_data['format']['duration'])))
        return duration

    def test_output_video_duration_should_match_input_duration(self, video_path):
        output_path = os.path.join(
            os.path.dirname(
                os.path.realpath(video_path)
            ),
            'mov.mp4'
        )
        encode_file(
            video_path,
            output_path,
            '1',
            '30',
            '480'
        )
        length1 = self.get_video_length(video_path)
        length2 = self.get_video_length(output_path)
        assert length1 == length2


Test().test_output_video_duration_should_match_input_duration('/tmp/mov.mp4')

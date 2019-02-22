import time
import queue
import random
import argparse
import subprocess
import multiprocessing
from threading import Thread, Lock

MAX_WORKER_THREADS = 3

FFMPEG_BINARY_PATH = 'ffmpeg'


FFMPEG_COMMAND_TEMPLATE = (
    'ffmpeg -y -i {input} -b:v {vid_bit_rate}M -r {fps} -s hd{res} {output}'
)


def encode_file(input_filename, output_filename, bit_rate, fps, res):
    cmd = FFMPEG_COMMAND_TEMPLATE.format(
        input=input_filename,
        output=output_filename,
        vid_bit_rate=bit_rate,
        fps=fps,
        res=res
    )
    cmd_args = cmd.split(' ')
    proc = subprocess.Popen(
        cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    while proc.poll() is None:
        time.sleep(
            random.randint(1, 3)
        )
    ret_code = proc.returncode
    return ret_code


class WorkerThread(Thread):

    def __init__(self, task_queue, worker_id):
        super().__init__()
        self._task_queue = task_queue
        self._worker_id = worker_id

    def run(self):
        while True:
            try:
                task_dict = self._task_queue.get(block=False)
            except queue.Empty:
                task_dict = None
                pass
            if task_dict is not None:
                if 'exit' in task_dict:
                    print(
                        'worker {} is shutting down'.format(
                            self._worker_id
                        )
                    )
                    break
                print(
                    'worker {}: starting encode of file {} to output file {}...'.format(
                        self._worker_id,
                        task_dict['input'],
                        task_dict['output']
                    )
                )
                ret_code = encode_file(
                    task_dict['input'],
                    task_dict['output'],
                    task_dict['bit_rate'],
                    task_dict['fps'],
                    task_dict['res']
                )
                # work_queue.task_done()
                if ret_code == 0:
                    print(
                        'worker {}: successfully completed encoding file {}....'.format(
                            self._worker_id,
                            task_dict['input']
                        )
                    )
                else:
                    print(
                        'worker {}: failed to encode file {} | return code {}'.format(
                            self._worker_id,
                            task_dict['input'],
                            ret_code
                        )
                    )
                self._task_queue.task_done()
            time.sleep(
                random.randint(1, 3)
            )


def get_tasks_from_job_file(path):
    task_list = []
    with open(path) as in_fh:
        for line in in_fh:
            line_parts = line.rstrip().split(',')
            task_list.append(
                {
                    'input': line_parts[0],
                    'output': line_parts[1],
                    'fps': int(line_parts[2]),
                    'bit_rate': int(line_parts[3]),
                    'res': int(line_parts[4])
                }
            )
    return task_list


def main(cmd_args):
    thread_list = []
    task_queue = queue.Queue()
    worker_count = int(cmd_args['workers'])
    job_file_path = cmd_args['job_file']
    print(
        'Reading encode tasks from job file {}...'.format(
            job_file_path
        )
    )
    task_list = get_tasks_from_job_file(
        job_file_path
    )
    for i in range(0, worker_count):
        thread_list.append(
            WorkerThread(task_queue, i)
        )
    print(
        'Starting {} worker thread(s)...'.format(
            worker_count
        )
    )
    for i in range(0, worker_count):
        thread_list[i].start()

    for task in task_list:
        task_queue.put(task)

    for i in range(0, worker_count):
        task_queue.put(
            {'exit': None}
        )
    print('Waiting for worker threads to finish')
    for i in range(0, worker_count):
        thread_list[i].join()


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Async IO hw assignment'
    )
    arg_parser.add_argument(
        'job_file',
        help=(
            'A CSV file containing the files to encode (format:'
            'input,output,fps,bit_rate,res)'
        )
    )
    arg_parser.add_argument(
        'workers',
        help=(
            'Max worker threads to spawn'
        )
    )
    main(vars(arg_parser.parse_args()))

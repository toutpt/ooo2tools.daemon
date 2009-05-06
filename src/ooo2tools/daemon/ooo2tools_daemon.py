import sys, time, os, re, commands, logging
from daemon import Daemon
from os import listdir, removedirs
from os.path import isdir, join
from tempfile import mkstemp
from stat import *
 
SHARED_DIR = '/home/alegros/share'
OUT_LOG = '/home/alegros/out.log'
CMD_EXE = 'python /home/alegros/ooo2tools.core/trunk/src/ooo2tools/core/footer.py --sequence='

logging.basicConfig(filename=OUT_LOG,level=logging.DEBUG,)
logger = logging.getLogger('Daemon')

class MyDaemon(Daemon):
    def run(self):
        logger.info('premiere boucle!')
        while True:
            if listdir(SHARED_DIR):
                files, todo_dirs = check_share()
                logger.info('todos found : ' + str(todo_dirs))
                first_task = task_to_process(todo_dirs)
                logger.info('task to process : ' + str(first_task))
                cmd_exe(first_task)
                time.sleep(1)

def check_share():
    """
    todo_dirs contain the absolute path names of the directories in
    SHARED_DIR that haven't got an associated '.lock' or '.processed' file.

    => []
    """
    todo_dirs = []
    files = [join(SHARED_DIR, item) for item in listdir(SHARED_DIR)]
    for item in files:
        if item + '.lock' not in files\
            and item + '.processed' not in files and isdir(item):
            todo_dirs.append(item)
    todo_dirs.sort()
    return todo_dirs

def task_to_process(todo_dirs):
    """
    finds the task with the most ancient modification
    time in todo_dirs
    
    * todo_dirs: obtained with check_share(), it contains
    path_names leading to tasks we want to execute.

    note : d contains the items (files) in todo_dirs
    as values, and their last modification time as their
    keys, so that d.get(min(d)) is the most ancient task

    => absolute path
    """
    first_task = ''
    d = dict(zip([os.stat(item)[ST_MTIME] for item in todo_dirs], todo_dirs))
    first_task = d.get(min(d))
    return first_task

def cmd_exe(first_task):
    """
    launch a bash command using ooo2tools.core to process
    the sequence file of first_task

    * first_task : obtained with task_to_process(),
    it is the task in SHARED_DIR with the most ancient
    modification time so we want it to be executed first

    => status integer and output message from the command
    """
    status = ''
    output = ''
    task = join(first_task, 'seq.txt')
    cmd = CMD_EXE + task
    logger.info('cmd : ' + cmd)
    status, output = commands.getstatusoutput(cmd)
    logger.info('status : ' + str(status) + '\n')
    if status == 0:
        f = open(join(first_task, '.processed'), 'w')
        f.close()
    return status, output

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

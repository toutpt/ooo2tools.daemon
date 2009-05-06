import doctest
import unittest
import os
import time
from os import mkdir, listdir, makedirs, utime
from os.path import join, exists
from shutil import copytree, rmtree
from ooo2tools.daemon.ooo2tools_daemon import check_share, task_to_process, cmd_exe
from ooo2tools.daemon import ooo2tools_daemon
from stat import *

SHARED_DIR = ooo2tools_daemon.SHARED_DIR

class Test_ooo2tools_daemon(unittest.TestCase):
    files = [join(SHARED_DIR, 'todo-000'),
        join(SHARED_DIR, 'todo-004'),
        join(SHARED_DIR, 'todo-002.processed'),
        join(SHARED_DIR, 'todo-003.lock'),
        join(SHARED_DIR, 'todo-003'),
        join(SHARED_DIR, 'todo-001'),
        join(SHARED_DIR, 'todo-003.processed'),
        join(SHARED_DIR, 'todo-002')]

    def setUp(self):
        self.files.sort()
        if exists(SHARED_DIR):
            rmtree(SHARED_DIR)
        mkdir(SHARED_DIR)
        for test_files in self.files:
            if '.processed' in test_files or '.lock' in test_files:
                f = open(join(SHARED_DIR, test_files), 'w')
                f.close()
            else:
                #copytree('test_todo', join(SHARED_DIR, test_files))
                copytree('test_todo', test_files)
        os.utime(self.files[0], (0,0))

    def test_check_share(self):
        todo = check_share()
        # we just keep files that have to be processed
        todo_dirs = [join(SHARED_DIR, 'todo-000'),
            join(SHARED_DIR, 'todo-004'),
            join(SHARED_DIR, 'todo-001')]
        for item in todo:
            self.assert_(item in todo_dirs, todo)

    def test_task_to_process(self):
        self.assertEqual(task_to_process(self.files), self.files[0])

    def test_cmd_exe(self):
        status, msg = cmd_exe(self.files[0])
        # 0 is the expected value if the command is executed without any problems
        self.assertEqual(status, 0)
        self.assert_('resultat.odt' in listdir(self.files[0]), msg)

    def tearDown(self):
        if exists(SHARED_DIR):
            rmtree(SHARED_DIR)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test_ooo2tools_daemon))
    return suite

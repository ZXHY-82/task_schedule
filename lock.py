"""
define '0' as unlock state
define '1' as lock state
"""


def check_lock(filename, lock_name):
    f = open(lock_name, 'r')
    line = f.readline()
    if line == '0':
        return 0
    else:
        return 1


def file_lock(filename, lock_name):
    f = open(lock_name, 'w')
    f.write('1')


def file_unlock(filename, lock_name):
    f = open(lock_name, 'w')
    f.write('0')


def ini_locks(lock_name):
    f = open(lock_name, 'w')
    f.write('0')



# -*- coding: UTF-8 -*-

import octo.filerecver as recver


def test_recv():
    assert recver.recv_file(9999, './recv_test_file') == True


# -*- coding: UTF-8 -*-

import octo.filesender as sender


def test_send():
    assert sender.send_file(9999, "./send_test_file") == True

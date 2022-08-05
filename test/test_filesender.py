# -*- coding: UTF-8 -*-

import octo.filetransfer.filesender as sender
import pytest


def test_send():
    assert sender.send_file("127.0.0.1", 9999, "./send_test_file") == True

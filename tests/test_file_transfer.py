# -*- coding: UTF-8 -*-

import octo.file_transfer_tcp as ft

PORT = 19302

def test_file_transfer_server():
    ft.run_server("./tests/send_test_file",PORT)

def test_file_transfer_client():
    ft.run_client("::1",PORT)



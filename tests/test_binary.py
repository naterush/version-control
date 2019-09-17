import pytest
import os
from saga.base_file.File import File
from saga.file_types.binary_file import parse_binary_file, write_binary_file
from saga.data_types.multi_dim_list.OP_MDL_Change import OP_MDL_Change

def create_binary_file(name, contents):
    if os.path.isfile(name):
        os.remove(name)
    f = open(name, 'w+b')
    f.write(bytearray(contents, 'utf-8'))
    f.close()

@pytest.fixture()
def setup_binary_files():
    if not os.path.isdir("temp"):
        os.mkdir('temp')
    create_binary_file("temp/binary0", "12345")

def test_create(setup_binary_files):
    binary_file = parse_binary_file("temp/binary0")
    assert binary_file.file_name == "temp/binary0"
    assert binary_file.file_contents.multi_dim_list[0] == '12345'

def test_create_then_write(setup_binary_files):
    binary_file = parse_binary_file("temp/binary0")
    write_binary_file(binary_file)
    f = open('temp/binary0', 'rb')
    assert f.read() == b'12345'

def test_get_operations_no_changechange(setup_binary_files):
    binary_file0 = parse_binary_file("temp/binary0")
    binary_file1 = parse_binary_file("temp/binary0")
    ops = binary_file0.get_operations(binary_file1)
    assert len(ops) == 0

def test_get_operations_change(setup_binary_files):
    binary_file0 = parse_binary_file("temp/binary0")
    create_binary_file("temp/binary0", "54321")
    binary_file1 = parse_binary_file("temp/binary0")
    ops = binary_file0.get_operations(binary_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Change)
import os
import pytest
from unittest.mock import MagicMock, patch
from pack import copy_with_progress, count_files

# Import the script's functions if they're in a separate module
# from your_module import count_files, copy_with_progress

def test_count_files(tmp_path):
    # Create a temporary directory structure
    (tmp_path / "subfolder").mkdir()
    (tmp_path / "subfolder" / "file1.txt").write_text("content")
    (tmp_path / "file2.txt").write_text("content")

    # Test count_files function
    assert count_files(tmp_path) == 2

def test_copy_with_progress_single_file(tmp_path, mocker):
    # Set up source and destination paths
    src = tmp_path / "source"
    dst = tmp_path / "destination"
    src.mkdir()
    dst.mkdir()
    file_path = src / "file.txt"
    file_path.write_text("content")

    # Mock the progress callback
    progress_callback = MagicMock()

    # Test copy_with_progress with a single file
    with patch('shutil.copy2') as mock_copy:
        copy_with_progress(str(src), str(dst), progress_callback)
        mock_copy.assert_called_once_with(str(file_path), str(dst / "file.txt"))
    progress_callback.assert_called_once_with(1, 1, f"Copying: {str(file_path)} to {str(dst / 'file.txt')}")

def test_copy_with_progress_directory(tmp_path, mocker):
    # Set up source and destination paths
    src = tmp_path / "source"
    dst = tmp_path / "destination"
    src.mkdir()
    dst.mkdir()
    sub_src = src / "subfolder"
    sub_src.mkdir()
    file_path = sub_src / "file.txt"
    file_path.write_text("content")

    # Mock the progress callback
    progress_callback = MagicMock()

    # Test copy_with_progress with directory structure
    with patch('shutil.copy2') as mock_copy:
        copy_with_progress(str(src), str(dst), progress_callback)
        mock_copy.assert_called_once_with(str(file_path), str(dst / "subfolder/file.txt"))
    assert progress_callback.call_count == 1

# Additional tests can be added for the pack function and more complex scenarios

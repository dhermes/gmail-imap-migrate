#!/usr/bin/env python

# Libraries
import os

# Local imports
import constants


CURR_DIR = os.path.dirname(__file__)


def main():
  old_data_dir_path = os.path.join(CURR_DIR, constants.OLD_DATA_DIR)
  if not os.path.exists(old_data_dir_path):
    print 'Making directory:', old_data_dir_path
    os.makedirs(old_data_dir_path)
  elif not os.path.isdir(old_data_dir_path):
    raise OSError('%s is not a directory.' % old_data_dir_path)
  else:
    print 'Directory', old_data_dir_path, 'exists, doing nothing.'

  new_data_dir_path = os.path.join(CURR_DIR, constants.NEW_DATA_DIR)
  if not os.path.exists(new_data_dir_path):
    print 'Making directory:', new_data_dir_path
    os.makedirs(new_data_dir_path)
  elif not os.path.isdir(new_data_dir_path):
    raise OSError('%s is not a directory.' % new_data_dir_path)
  else:
    print 'Directory', new_data_dir_path, 'exists, doing nothing.'


if __name__ == '__main__':
  main()


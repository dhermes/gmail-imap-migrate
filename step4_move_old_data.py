#!/usr/bin/env python

# Libraries
import imapclient
import json
import os
import re

# Local imports
import account_settings
import constants
import utils


RELABEL_MAP = {
    '[Gmail]/Chats': account_settings.CHATS_NEW_LABEL,
}
CURR_DIR = os.path.dirname(__file__)
MIGRATION_PROGRESS_FI = os.path.join(CURR_DIR, constants.NEW_DATA_DIR,
                                     constants.MIGRATION_PROGRESS_FI)
PRINT_INTERVAL = 500


def store_migration_progress(migration_progress):
  with open(MIGRATION_PROGRESS_FI, 'w') as fh:
    json.dump(migration_progress, fh)


def read_migration_progress():
  if not os.path.exists(MIGRATION_PROGRESS_FI):
    migration_progress = {}
    store_migration_progress(migration_progress)
  else:
    with open(MIGRATION_PROGRESS_FI, 'r') as fh:
      migration_progress = json.load(fh)

  return migration_progress


def get_new_folder_msg_id(folder_uid, append_status):
  append_status_template = (r'^\[APPENDUID %d (\d+)\] \(Success\)$' %
                            folder_uid)
  match = re.match(append_status_template, append_status)
  return int(match.groups()[0])


def add_msg_to_new_account(msg_data_dict, folder_new, folder_uid,
                           server_old, server_new):
  msg_id = msg_data_dict['msg_id']

  other_folders = msg_data_dict['other_folders']
  folder_msg_id = msg_data_dict['folder_msg_id']

  # Get the message from the old folder / account.
  msg_contents = server_old.fetch([folder_msg_id],
                                  constants.FULL_MSG_FIELDS)
  flags = msg_contents[folder_msg_id][constants.FLAGS_FIELD]
  msg = msg_contents[folder_msg_id][constants.FULL_MSG_FIELD]
  msg_time = msg_contents[folder_msg_id][constants.DATE_FIELD]

  # Add the message to the new account.
  append_status = server_new.append(folder_new, msg.encode('utf-8'),
                                    flags=flags, msg_time=msg_time)
  new_folder_msg_id = get_new_folder_msg_id(folder_uid, append_status)
  for other_folder, _ in other_folders:
    server_new.copy([new_folder_msg_id], other_folder)


def migrate(folder_data, migration_progress, server_old, server_new):
  total_msgs = sum([len(val) for val in folder_data.values()
                    if val is not None])
  count = 0
  for folder, gmail_msg_dict in folder_data.iteritems():
    print 'Beginning', folder
    list_of_completed = migration_progress.setdefault(folder, [])

    # Open folders for files.
    server_old.select_folder(folder, readonly=True)
    folder_new = folder
    if folder in RELABEL_MAP:
      print 'Re-labeling new folder.'
      folder_new = RELABEL_MAP[folder]

    new_folder_info = server_new.select_folder(folder_new)
    folder_uid = new_folder_info['UIDVALIDITY']

    for gmail_id, msg_data_dict in gmail_msg_dict.iteritems():
      count += 1
      if count % PRINT_INTERVAL == 0:
        print 'Folder: %s, Gmail ID: %s, %d / %d' % (folder, gmail_id,
                                                     count, total_msgs)

      if gmail_id in list_of_completed:
        continue

      add_msg_to_new_account(msg_data_dict, folder_new, folder_uid,
                             server_old, server_new)
      list_of_completed.append(gmail_id)
      store_migration_progress(migration_progress)


def main():
  folder_data_fi = os.path.join(CURR_DIR, constants.OLD_DATA_DIR,
                                constants.FOLDER_DATA_FI)
  with open(folder_data_fi, 'r') as fh:
    folder_data = json.load(fh)

  migration_progress = read_migration_progress()

  # Log-in to both old and new servers.
  server_old = utils.login_to_server(account_settings.OLD_USERNAME,
                                     account_settings.OLD_PASSWORD)
  server_new = utils.login_to_server(account_settings.NEW_USERNAME,
                                     account_settings.NEW_PASSWORD)
  migrate(folder_data, migration_progress, server_old, server_new)

  # Log-out of both servers.
  server_old.logout()
  server_new.logout()


if __name__ == '__main__':
  main()

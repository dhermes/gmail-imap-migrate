#!/usr/bin/env python

# Libraries
import imapclient
import imaplib
import json
import os

# Local imports
import account_settings
import constants
import utils


# Ordered tuple of folders which we need to consider first since
# we expect them to be the most common.
SPECIAL_FOLDERS = ('[Gmail]/All Mail', 'INBOX')
CURR_DIR = os.path.dirname(__file__)


def save_old_folders(server):
  all_folders_fi = os.path.join(CURR_DIR, constants.OLD_DATA_DIR,
                                constants.ALL_FOLDERS_FI)
  if os.path.exists(all_folders_fi):
    raise OSError('All folders file: %s already exists.' % all_folders_fi)

  print 'Getting all folders'
  all_folders = server.list_folders()
  all_folders = [triple[2] for triple in all_folders]

  # Remove the special folders from the list.
  for folder in SPECIAL_FOLDERS:
    all_folders.remove(folder)

  # Put the special folders in front (in reverse order so the first
  # is the last to be put in front).
  for folder in reversed(SPECIAL_FOLDERS):
    all_folders.insert(0, folder)

  print '=' * 70

  print 'Saving', all_folders_fi
  with open(all_folders_fi, 'w') as fh:
    json.dump(all_folders, fh)
  print 'Saved', all_folders_fi

  return all_folders


def get_current_folder_data(server, folder, msg_to_folder, folder_data):
  current_folder_data = {}

  # Have to use readonly=True since some folders (like Chats) are READONLY.
  try:
    server.select_folder(folder, readonly=True)
  except imaplib.IMAP4.error as err:
    print 'Folder', folder, 'does not exist'
    print 'Error:', err
    return

  print 'Getting folder local message IDs'
  folder_msg_ids = server.search()
  print 'Retrieved %d message IDs.' % len(folder_msg_ids)
  print 'Getting all "Message-ID" headers and Gmail Message IDs.'
  folder_msg_contents = server.fetch(
      folder_msg_ids, [constants.GMAIL_ID_FIELD, constants.MSG_ID_FIELD])

  print 'Adding message data to dictionary'
  for folder_msg_id, msg_dict in folder_msg_contents.iteritems():
    gmail_msg_id = msg_dict[constants.GMAIL_ID_FIELD]
    msg_id = msg_dict[constants.MSG_ID_KEY]

    if gmail_msg_id in msg_to_folder:
      # Update the message entry in the original folder.
      actual_folder = msg_to_folder[gmail_msg_id]
      actual_folder_data = folder_data[actual_folder]
      # Update the message entry in the original folder.
      actual_msg_entry = actual_folder_data[gmail_msg_id]
      actual_msg_entry['other_folders'].append((folder, folder_msg_id))
      # Make sure data agrees.
      if actual_msg_entry['msg_id'] != msg_id:
        raise ValueError('Mis-matching message IDs for same message.')
    else:
      msg_to_folder[gmail_msg_id] = folder
      current_folder_data[gmail_msg_id] = {'msg_id': msg_id,
                                           'other_folders': [],
                                           'folder_msg_id': folder_msg_id}

  return current_folder_data


def get_all_folder_data(server, all_folders):
  folder_data_fi = os.path.join(CURR_DIR, constants.OLD_DATA_DIR,
                                constants.FOLDER_DATA_FI)
  if os.path.exists(folder_data_fi):
    raise OSError('Folder data file: %s already exists.' % folder_data_fi)

  msg_to_folder = {}
  folder_data = {}
  for folder in all_folders:
    print '=' * 70
    print 'Beginning folder:', folder
    current_folder_data = get_current_folder_data(server, folder,
                                                  msg_to_folder, folder_data)
    folder_data[folder] = current_folder_data

  print '=' * 70

  print 'Saving', folder_data_fi
  with open(folder_data_fi, 'w') as fh:
    json.dump(folder_data, fh)
  print 'Saved', folder_data_fi

  return folder_data


def main():
  server = utils.login_to_server(account_settings.OLD_USERNAME,
                                 account_settings.OLD_PASSWORD)
  all_folders = save_old_folders(server)
  folder_data = get_all_folder_data(server, all_folders)
  server.logout()


if __name__ == '__main__':
  main()

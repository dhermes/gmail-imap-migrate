#!/usr/bin/env python

# Libraries
import imapclient

# Local imports
import account_settings
import utils


def get_all_folders(username, password):
  server = utils.login_to_server(username, password)

  all_folders = server.list_folders()
  all_folders = [triple[2] for triple in all_folders]

  return all_folders, server


def main():
  all_folders_old, server_old = get_all_folders(
      account_settings.OLD_USERNAME, account_settings.OLD_PASSWORD)
  # We don't need the old server connection any longer.
  server_old.logout()

  all_folders_new, server_new = get_all_folders(
      account_settings.NEW_USERNAME, account_settings.NEW_PASSWORD)

  uncreated_old_folders = set(all_folders_old).difference(all_folders_new)

  for folder in uncreated_old_folders:
    server_new.create_folder(folder)
    print 'Created', folder

  server_new.logout()


if __name__ == '__main__':
  main()

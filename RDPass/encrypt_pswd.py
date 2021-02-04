import argparse
import configparser
import os
import os.path
from base64 import urlsafe_b64encode, urlsafe_b64decode
from getpass import getpass

#from simplecrypt import decrypt, encrypt


def encrypt_text(decrypt_password, plaintext):
    cipher = decrypt_password #encrypt(decrypt_password, plaintext)
    encoded_cipher = urlsafe_b64encode(bytes(cipher,'utf-8'))
    return encoded_cipher.decode('utf-8')


def decrypt_text(decrypt_password, encoded_cipher):
    cipher = b64decode(encoded_cipher)
    plaintext = cipher  #decrypt(decrypt_password, cipher)
    return plaintext.decode('utf-8')


def encrypt_config_file(input_file, output_file, decrypt_password):
    """Takes in an unencrypted config file and writes an encrypted config file given the decryption password."""
    config = configparser.RawConfigParser()
    config.read(input_file)

    for section in config.sections():
        section = config[section]
        for key in section.keys():
            value = section[key]
            section[key] = encrypt_text(decrypt_password, value)

    with open(output_file, 'w') as f:
        config.write(f)


def write_config_file(config_filename, credential_name, cred_type=['user', 'password']):
    # Check if decryption password exists in environment
    if os.environ.get("SATS_PWD") is None:
        decryption_password = getpass(prompt='decryption_password')
    else:
        decryption_password = os.environ["SATS_PWD"]
    cred_dict = add_config_section(config_filename, credential_name, decryption_password, cred_type)
    return cred_dict


def input_credentials(credential_name, cred_type):
    cred_dict = {}
    for cred in cred_type:
        input_cred = getpass(prompt="{credential_name} {cred}".format(credential_name=credential_name, cred=cred))
        cred_dict.update({cred: input_cred})
    return cred_dict


def add_config_section(config_filename, credential_name, decryption_password, cred_type):
    # create a new section (eg. sql_database) and add credential types (eg api key)
    config = configparser.RawConfigParser()
    config.read(config_filename)
    config.add_section(credential_name)
    cred_dict = add_cred_to_section(config_filename, config, credential_name, decryption_password, cred_type)
    return cred_dict


def add_cred_to_section(config_filename, config, credential_name, decryption_password, cred_type):
    # add a credential type under a particular section (eg add user to section sql_database)
    cred_dict = input_credentials(credential_name, cred_type)
    for key, value in cred_dict.items():
        config.set(credential_name, key, encrypt_text(decryption_password, value))
    cfile = open(config_filename, "w")
    config.write(cfile)
    cfile.close()
    return cred_dict


def read_config_file(config_filename, credential_name, cred_type=[]):
    config = configparser.RawConfigParser()
    config.read(config_filename)
    # Check if decryption password exists in environment
    if os.environ.get("SATS_PWD") is None:
        decrypt_password = getpass(prompt='decrypt_password')
    else:
        decrypt_password = os.environ["SATS_PWD"]
    cred_dict = {}

    if len(cred_type) == 0:
        section = config[credential_name]
        for key in section.keys():
            value = section[key]
            cred_dict[key] = decrypt_text(decrypt_password, value)

    # TODO: This section is not very obvious this should be done by this function
    # loop through credentials in an existing section and write credential if there is none
    for cred in cred_type:
        try:
            cred_dict.update({cred: decrypt_text(decrypt_password, config.get(credential_name, cred))})
        except configparser.NoOptionError:
            cred_dict = add_cred_to_section(config_filename, config, credential_name, decrypt_password, cred_type)
    return cred_dict


def grab_credentials_from_config(config_file, credential_name, cred_type=['user', 'password']):
    """returns a dictionary of credentials (cred_type) under a spectic section (credential name)
       checks if a config file exists and if the credential name and type already exists and
       if not allows input into config file for later use"""
    if os.path.isfile(config_file):
        try:
            cred_dict = read_config_file(config_file, credential_name, cred_type)
        except configparser.NoSectionError:
            cred_dict = write_config_file(config_file, credential_name, cred_type)
    else:
        cred_dict = write_config_file(config_file, credential_name, cred_type)
    return cred_dict


if __name__ == "__main__":
    """ Usecase of these functions. Pass the username and password to arguements so they can be used
    for eg. get_database_engine(user=user, password=password)"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", default="config.ini")
    parser.add_argument("--credential_name", required=True, help='eg. sql_database')
    args = parser.parse_args()
    credentials = grab_credentials_from_config(args.config_file, args.credential_name)
    user = credentials["user"]
    password = credentials["password"]

    # google maps api key example
    credentials = grab_credentials_from_config(args.config_file, 'google maps', cred_type=['api_key'])
    api_key = credentials["api_key"]

    credentials = grab_credentials_from_config(args.config_file, 'google maps', cred_type=['password'])
    api_key = credentials["password"]

from cryptography.fernet import Fernet
import hashlib
import json
import os
from datetime import datetime

def encrypt_file(input_file):
    try:

        key = Fernet.generate_key()
        fernet = Fernet(key)

        with open(input_file, 'rb') as file:
            original_data = file.read()

        hash_obj = hashlib.sha256(original_data)
        hash_value = hash_obj.hexdigest()

        encrypted_data = fernet.encrypt(original_data)

        output_dir = os.path.dirname(input_file)

        encrypt_file_path = os.path.join(output_dir, 'encrypted_file.bin')
        with open(encrypt_file, 'wb') as file:
            file.write(encrypted_data)

        metadata = {
            'key': key.decode('utf-8'),
            'hash': hash_value,
            'original_filename' : os.path.basename(input_file),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        metadata_path = os.path.join(output_dir, 'encryption_metadata.json')
        with open(metadata_path, 'w') as file:
            json.dump(metadata, file, indent=4)

        print('File encrypted successfully')
        print(f'Encrypted file:, {encrypt_file_path}')
        print(f'金鑰和雜湊值儲存於: {metadata_path}')
        print(f'原始檔案雜湊值: {hash_value}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    input_file = 'sample.txt'
    encrypt_file(input_file)
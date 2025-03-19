from cryptography.fernet import Fernet
import hashlib
import json
import os

def decrypt_and_verify(encrypted_file_path, metadata_path, output_dir):
    try:
        with open(metadata_path, 'r') as file:
            metadata = json.load(file)
        
        key = metadata['key'].encode('utf-8')
        original_hash = metadata['original_filename']
        original_filename = metadata['original_filename']

        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()

        encrypted_hash = hashlib.sha256(encrypted_data).hexdigest()
        print(f'加密檔案的雜湊值: {encrypted_hash}')

        fernet = Fernet(key)

        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            print('解密成功')
        except Exception as e:
            print(f'解密失敗: {str(e)}')
            print('原因:加密檔案可能已被修改，導致無法正確解密')
            return

        decrypted_hash = hashlib.sha256(decrypted_data).hexdigest()
        print(f'解密檔案的雜湊值: {decrypted_hash}')
        print(f'原始檔案的雜湊值: {original_hash}')

        if decrypted_hash == original_hash:
            print('檔案完整性驗證成功')
        else:
            print('檔案完整性驗證失敗')
            return
        decrypted_file_path = os.path.join(output_dir, f'decrypted_{original_filename}')
        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)
        
        print(f'解密檔案儲存於: {decrypted_file_path}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    encrypted_file_path = 'sample.txt'
    metadata_path = 'encryption_metadata.json'
    output_dir = os.path.dirname(encrypted_file_path)
    decrypt_and_verify(encrypted_file_path, metadata_path, output_dir)
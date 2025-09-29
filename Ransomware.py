#!/usr/bin/env python3
"""
DEMOSTRACIÓN CON VERIFICACIÓN DE ENCRIPTACIÓN EN TIEMPO REAL
"""

import os
import time
import hashlib
from cryptography.fernet import Fernet

class RansomwareDemoConVerificacion:
    def __init__(self):
        self.target_folder = "/tmp/ransomware_demo/"
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.hashes_originales = {}
        self.hashes_cifrados = {}
        
    def calcular_hash(self, datos):
        """Calcula hash SHA-256 para verificación"""
        return hashlib.sha256(datos).hexdigest()[:16]  # Primeros 16 chars

    def crear_archivos_prueba(self):
        """Crea archivos de prueba y guarda sus hashes"""
        os.makedirs(self.target_folder, exist_ok=True)
        
        archivos_prueba = {
            "documento.txt": "Este es un documento de prueba para la demostración.",
            "foto.jpg.demo": "Contenido simulado de imagen " + "x" * 100,
            "datos.xlsx.demo": "Datos de prueba para Excel " + "y" * 50
        }
        
        for nombre, contenido in archivos_prueba.items():
            ruta = os.path.join(self.target_folder, nombre)
            with open(ruta, 'w') as f:
                f.write(contenido)
            
            # Calcular y guardar hash original
            with open(ruta, 'rb') as f:
                self.hashes_originales[nombre] = self.calcular_hash(f.read())
            
            print(f"✓ Creado: {nombre} | Hash: {self.hashes_originales[nombre]}")
    
    def verificar_estado_archivos(self, fase):
        """Verifica y muestra el estado actual de los archivos"""
        print(f"\n🔍 VERIFICACIÓN - {fase}:")
        print("-" * 50)
        
        for archivo in os.listdir(self.target_folder):
            ruta = os.path.join(self.target_folder, archivo)
            if os.path.isfile(ruta):
                with open(ruta, 'rb') as f:
                    contenido = f.read()
                    hash_actual = self.calcular_hash(contenido)
                    tamaño = len(contenido)
                    
                    # Verificar si es cifrado o original
                    estado = "CIFRADO" if archivo.endswith('.cifrado') else "ORIGINAL"
                    
                    print(f"📁 {archivo}")
                    print(f"   Estado: {estado}")
                    print(f"   Tamaño: {tamaño} bytes")
                    print(f"   Hash: {hash_actual}")
                    
                    # Comparar con hash original si existe
                    nombre_base = archivo.replace('.cifrado', '')
                    if nombre_base in self.hashes_originales:
                        if hash_actual == self.hashes_originales[nombre_base]:
                            print(f"   ✅ COINCIDENCIA con original")
                        else:
                            print(f"   ❌ DIFERENTE al original")
                    print()

    def cifrar_archivos_con_verificacion(self):
        """Cifra archivos mostrando verificación paso a paso"""
        print("🔒 INICIANDO CIFRADO CON VERIFICACIÓN...")
        
        # Verificación ANTES del cifrado
        self.verificar_estado_archivos("ANTES DEL CIFRADO")
        
        input("\n⏸️  Presiona Enter para proceder con el cifrado...")
        
        for archivo in os.listdir(self.target_folder):
            ruta_completa = os.path.join(self.target_folder, archivo)
            
            if os.path.isfile(ruta_completa) and not archivo.endswith('.cifrado'):
                print(f"\n🔄 Cifrando: {archivo}")
                
                # Leer y mostrar datos originales
                with open(ruta_completa, 'rb') as f:
                    datos_originales = f.read()
                
                print(f"   Contenido original (primeros 50 bytes): {datos_originales[:50]}")
                print(f"   Hash original: {self.calcular_hash(datos_originales)}")
                
                # Cifrar
                datos_cifrados = self.cipher.encrypt(datos_originales)
                self.hashes_cifrados[archivo] = self.calcular_hash(datos_cifrados)
                
                print(f"   Contenido cifrado (primeros 50 bytes): {datos_cifrados[:50]}")
                print(f"   Hash cifrado: {self.hashes_cifrados[archivo]}")
                
                # Guardar archivo cifrado
                nuevo_nombre = archivo + ".cifrado"
                with open(os.path.join(self.target_folder, nuevo_nombre), 'wb') as f:
                    f.write(datos_cifrados)
                
                # Eliminar original
                os.remove(ruta_completa)
                print(f"   ✅ {archivo} → {nuevo_nombre}")
        
        # Verificación DESPUÉS del cifrado
        print("\n" + "="*60)
        self.verificar_estado_archivos("DESPUÉS DEL CIFRADO")

    def demostrar_lectura_cifrada(self):
        """Demuestra que los archivos cifrados son ilegibles"""
        print("\n📖 DEMOSTRACIÓN DE LECTURA DE ARCHIVOS CIFRADOS:")
        print("-" * 50)
        
        for archivo in os.listdir(self.target_folder):
            if archivo.endswith('.cifrado'):
                ruta = os.path.join(self.target_folder, archivo)
                
                print(f"\n📁 Intentando leer: {archivo}")
                
                try:
                    with open(ruta, 'rb') as f:
                        contenido_cifrado = f.read()
                    
                    # Intentar leer como texto (debería fallar)
                    try:
                        texto_intento = contenido_cifrado.decode('utf-8')
                        print(f"   ❌ ERROR: Se pudo decodificar como texto (no debería pasar)")
                    except UnicodeDecodeError:
                        print(f"   ✅ Correcto: No se puede decodificar como texto")
                    
                    # Mostrar contenido cifrado
                    print(f"   Contenido cifrado (hex): {contenido_cifrado[:30].hex()}...")
                    print(f"   Tamaño cifrado: {len(contenido_cifrado)} bytes")
                    
                except Exception as e:
                    print(f"   ❌ Error leyendo archivo: {e}")

    def descifrar_archivos_con_verificacion(self):
        """Descifra mostrando verificación de integridad"""
        print("\n🔓 INICIANDO DESCIFRADO CON VERIFICACIÓN...")
        
        # Verificación antes del descifrado
        self.verificar_estado_archivos("ANTES DEL DESCIFRADO")
        
        input("\n⏸️  Presiona Enter para proceder con el descifrado...")
        
        for archivo in os.listdir(self.target_folder):
            if archivo.endswith(".cifrado"):
                ruta_completa = os.path.join(self.target_folder, archivo)
                
                print(f"\n🔄 Descifrando: {archivo}")
                
                with open(ruta_completa, 'rb') as f:
                    datos_cifrados = f.read()
                
                print(f"   Hash antes de descifrar: {self.calcular_hash(datos_cifrados)}")
                
                try:
                    # Descifrar
                    datos_originales = self.cipher.decrypt(datos_cifrados)
                    nombre_original = archivo.replace(".cifrado", "")
                    
                    print(f"   Hash después de descifrar: {self.calcular_hash(datos_originales)}")
                    print(f"   Hash original guardado: {self.hashes_originales.get(nombre_original, 'No encontrado')}")
                    
                    # Verificar integridad
                    hash_actual = self.calcular_hash(datos_originales)
                    hash_original = self.hashes_originales.get(nombre_original)
                    
                    if hash_actual == hash_original:
                        print(f"   ✅ INTEGRIDAD VERIFICADA: Los datos son idénticos al original")
                    else:
                        print(f"   ❌ ERROR DE INTEGRIDAD: Los datos no coinciden")
                    
                    # Guardar archivo recuperado
                    with open(os.path.join(self.target_folder, nombre_original), 'wb') as f:
                        f.write(datos_originales)
                    
                    os.remove(ruta_completa)
                    print(f"   ✅ Recuperado exitosamente: {nombre_original}")
                    
                except Exception as e:
                    print(f"   ❌ Error descifrando {archivo}: {e}")
        
        # Verificación final
        print("\n" + "="*60)
        self.verificar_estado_archivos("DESPUÉS DEL DESCIFRADO")

    def ejecutar_demo_completa(self):
        """Ejecuta la demostración completa con verificación"""
        print("🚨 DEMOSTRACIÓN CON VERIFICACIÓN EN TIEMPO REAL 🚨")
        print("=" * 60)
        
        # Fase 1: Preparación
        print("\n1️⃣  CREANDO ARCHIVOS DE PRUEBA...")
        self.crear_archivos_prueba()
        
        input("\n⏸️  Presiona Enter para iniciar fase de cifrado...")
        
        # Fase 2: Cifrado con verificación
        print("\n2️⃣  FASE DE CIFRADO (SIMULACIÓN DE ATAQUE)")
        self.cifrar_archivos_con_verificacion()
        
        # Fase 3: Demostración de ilegibilidad
        print("\n3️⃣  DEMOSTRANDO QUE LOS ARCHIVOS SON ILEGIBLES")
        self.demostrar_lectura_cifrada()
        
        input("\n⏸️  Presiona Enter para mostrar mensaje de rescate...")
        
        # Fase 4: Mensaje de rescate
        print("\n4️⃣  MENSAJE DE RESCATE SIMULADO")
        mensaje_rescate = f"""
        ⚠️  ¡TUS ARCHIVOS HAN SIDO CIFRADOS! ⚠️
        
        Para verificar el cifrado:
        - Los archivos tienen extensión .cifrado
        - No se pueden abrir con programas normales
        - El contenido es ilegible
        - Los hashes SHA-256 han cambiado completamente
        
        Clave de demostración: {self.key.decode()}
        """
        print(mensaje_rescate)
        
        input("\n⏸️  Presiona Enter para proceder con la recuperación...")
        
        # Fase 5: Recuperación con verificación
        print("\n5️⃣  FASE DE RECUPERACIÓN CON CLAVE CORRECTA")
        self.descifrar_archivos_con_verificacion()
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")

# Ejecutar demostración
if __name__ == "__main__":
    demo = RansomwareDemoConVerificacion()
    demo.ejecutar_demo_completa()
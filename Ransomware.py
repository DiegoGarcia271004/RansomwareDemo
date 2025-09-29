#!/usr/bin/env python3
"""
DEMOSTRACIÓN CON VERIFICACIÓN MEJORADA DE CIFRADO
"""

import os
import time
import hashlib
import string
from cryptography.fernet import Fernet

class RansomwareDemoVerificacionReal:
    def __init__(self):
        self.target_folder = "/tmp/ransomware_demo/"
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.hashes_originales = {}
        
    def calcular_hash(self, datos):
        """Calcula hash SHA-256 para verificación"""
        return hashlib.sha256(datos).hexdigest()[:16]

    def es_texto_legible(self, datos):
        """Verifica si los datos son texto legible"""
        try:
            texto = datos.decode('utf-8', errors='ignore')
            # Contar caracteres imprimibles
            caracteres_imprimibles = sum(1 for c in texto if c in string.printable)
            porcentaje_legible = (caracteres_imprimibles / len(texto)) * 100
            return porcentaje_legible > 80.0  # Si más del 80% es legible
        except:
            return False

    def analizar_entropia(self, datos):
        """Analiza la entropía para detectar datos cifrados"""
        if len(datos) == 0:
            return 0
        
        # Calcular frecuencia de bytes
        freq = {}
        for byte in datos:
            freq[byte] = freq.get(byte, 0) + 1
        
        # Calcular entropía
        entropia = 0
        for count in freq.values():
            p = count / len(datos)
            entropia -= p * (p and (p).log2())  # Evitar log(0)
        
        return entropia

    def crear_archivos_prueba(self):
        """Crea archivos de prueba variados"""
        os.makedirs(self.target_folder, exist_ok=True)
        
        archivos_prueba = {
            "documento.txt": "Este es un documento de prueba importante para la demostración.",
            "contraseñas.txt": "usuario: admin\ncontraseña: Demo123!\nemail: test@demo.com",
            "datos_sensibles.csv": "nombre,edad,saldo\nJuan,30,5000\nMaria,25,3000",
            "imagen.jpg.demo": b"JFIF" + b"\xff" * 100,  # Simular header de JPEG
            "base_datos.db.demo": b"SQLite" + b"\x00" * 50  # Simular archivo binario
        }
        
        for nombre, contenido in archivos_prueba.items():
            ruta = os.path.join(self.target_folder, nombre)
            
            if isinstance(contenido, str):
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                # Guardar también en bytes para hash consistente
                contenido_bytes = contenido.encode('utf-8')
            else:
                with open(ruta, 'wb') as f:
                    f.write(contenido)
                contenido_bytes = contenido
            
            self.hashes_originales[nombre] = self.calcular_hash(contenido_bytes)
            print(f"✓ Creado: {nombre} | Hash: {self.hashes_originales[nombre]}")

    def verificar_archivo_detallado(self, ruta_archivo, nombre_archivo):
        """Verificación detallada de un archivo individual"""
        with open(ruta_archivo, 'rb') as f:
            contenido = f.read()
        
        hash_actual = self.calcular_hash(contenido)
        tamaño = len(contenido)
        es_legible = self.es_texto_legible(contenido)
        entropia = self.analizar_entropia(contenido)
        
        print(f"📁 {nombre_archivo}")
        print(f"   Tamaño: {tamaño} bytes")
        print(f"   Hash: {hash_actual}")
        print(f"   ¿Texto legible?: {'✅ SÍ' if es_legible else '❌ NO'}")
        print(f"   Entropía: {entropia:.2f} bits")
        
        # Mostrar preview del contenido
        if es_legible:
            try:
                preview = contenido.decode('utf-8', errors='ignore')[:60]
                print(f"   Preview: '{preview}...'")
            except:
                print(f"   Preview: [No se puede decodificar]")
        else:
            print(f"   Preview (hex): {contenido[:30].hex()}...")
        
        # Comparar con original si existe
        nombre_base = nombre_archivo.replace('.cifrado', '')
        if nombre_base in self.hashes_originales:
            if hash_actual == self.hashes_originales[nombre_base]:
                print(f"   🔄 Estado: IDÉNTICO al original")
            else:
                print(f"   🔄 Estado: MODIFICADO (cifrado)")
        
        print()

    def cifrar_archivos_con_verificacion(self):
        """Cifrado con verificación mejorada"""
        print("🔒 INICIANDO CIFRADO CON VERIFICACIÓN MEJORADA...")
        
        print("\n📊 ESTADO INICIAL DE ARCHIVOS:")
        print("=" * 50)
        for archivo in os.listdir(self.target_folder):
            if os.path.isfile(os.path.join(self.target_folder, archivo)):
                self.verificar_archivo_detallado(
                    os.path.join(self.target_folder, archivo), 
                    archivo
                )
        
        input("\n⏸️  Presiona Enter para proceder con el cifrado...")
        
        for archivo in os.listdir(self.target_folder):
            ruta_completa = os.path.join(self.target_folder, archivo)
            
            if os.path.isfile(ruta_completa) and not archivo.endswith('.cifrado'):
                print(f"\n🔄 Cifrando: {archivo}")
                
                with open(ruta_completa, 'rb') as f:
                    datos_originales = f.read()
                
                # Mostrar análisis antes
                print(f"   ANTES - Legible: {self.es_texto_legible(datos_originales)}")
                print(f"   ANTES - Entropía: {self.analizar_entropia(datos_originales):.2f}")
                
                # Cifrar
                datos_cifrados = self.cipher.encrypt(datos_originales)
                
                # Mostrar análisis después
                print(f"   DESPUÉS - Legible: {self.es_texto_legible(datos_cifrados)}")
                print(f"   DESPUÉS - Entropía: {self.analizar_entropia(datos_cifrados):.2f}")
                
                # Guardar cifrado
                nuevo_nombre = archivo + ".cifrado"
                with open(os.path.join(self.target_folder, nuevo_nombre), 'wb') as f:
                    f.write(datos_cifrados)
                
                os.remove(ruta_completa)
                print(f"   ✅ {archivo} → {nuevo_nombre}")
        
        print("\n📊 ESTADO FINAL DE ARCHIVOS (CIFRADOS):")
        print("=" * 50)
        for archivo in os.listdir(self.target_folder):
            if os.path.isfile(os.path.join(self.target_folder, archivo)):
                self.verificar_archivo_detallado(
                    os.path.join(self.target_folder, archivo), 
                    archivo
                )

    def demostrar_ilegibilidad(self):
        """Demostración práctica de que no se pueden usar los archivos"""
        print("\n🚫 DEMOSTRACIÓN PRÁCTICA DE ILEGIBILIDAD:")
        print("=" * 50)
        
        for archivo in os.listdir(self.target_folder):
            if archivo.endswith('.cifrado'):
                ruta = os.path.join(self.target_folder, archivo)
                nombre_base = archivo.replace('.cifrado', '')
                
                print(f"\n🎯 Intentando usar: {archivo} como {nombre_base}")
                
                with open(ruta, 'rb') as f:
                    contenido_cifrado = f.read()
                
                # Intentar usar según el tipo de archivo original
                if nombre_base.endswith('.txt') or nombre_base.endswith('.csv'):
                    print("   📝 Intentando leer como texto...")
                    try:
                        texto = contenido_cifrado.decode('utf-8')
                        print(f"   ❌ INESPERADO: Se pudo leer como texto")
                        print(f"   Contenido: {texto[:100]}...")
                    except UnicodeDecodeError:
                        print("   ✅ CORRECTO: No se puede decodificar como texto")
                
                elif nombre_base.endswith('.jpg.demo'):
                    print("   🖼️  Intentando detectar como imagen...")
                    # Verificar header de JPEG
                    if contenido_cifrado.startswith(b'\xff\xd8\xff'):
                        print("   ✅ Parece ser una imagen JPEG válida")
                    else:
                        print("   ❌ No es una imagen JPEG válida")
                
                elif nombre_base.endswith('.db.demo'):
                    print("   💾 Intentando detectar como base de datos...")
                    if contenido_cifrado.startswith(b'SQLite'):
                        print("   ✅ Parece ser una base de datos SQLite")
                    else:
                        print("   ❌ No es una base de datos SQLite válida")
                
                # Mostrar diferencia práctica
                print(f"   🔍 Conclusión: El archivo {nombre_base} es INUTILIZABLE")

    def descifrar_y_verificar(self):
        """Descifrado con verificación de utilidad"""
        print("\n🔓 DESCIFRADO Y VERIFICACIÓN DE UTILIDAD:")
        print("=" * 50)
        
        for archivo in os.listdir(self.target_folder):
            if archivo.endswith(".cifrado"):
                ruta_completa = os.path.join(self.target_folder, archivo)
                nombre_original = archivo.replace(".cifrado", "")
                
                print(f"\n🔄 Descifrando: {archivo}")
                
                with open(ruta_completa, 'rb') as f:
                    datos_cifrados = f.read()
                
                try:
                    datos_originales = self.cipher.decrypt(datos_cifrados)
                    
                    # Verificar integridad
                    hash_actual = self.calcular_hash(datos_originales)
                    hash_esperado = self.hashes_originales.get(nombre_original)
                    
                    # Guardar archivo recuperado
                    if nombre_original.endswith('.demo'):  # Archivos binarios
                        with open(os.path.join(self.target_folder, nombre_original), 'wb') as f:
                            f.write(datos_originales)
                    else:  # Archivos de texto
                        with open(os.path.join(self.target_folder, nombre_original), 'w', encoding='utf-8') as f:
                            f.write(datos_originales.decode('utf-8'))
                    
                    os.remove(ruta_completa)
                    
                    # Verificar utilidad
                    print(f"   ✅ Descifrado exitoso")
                    print(f"   🔍 Integridad: {'✅ VERIFICADA' if hash_actual == hash_esperado else '❌ CORRUPTO'}")
                    print(f"   📊 Utilidad: {'✅ RECUPERADO' if self.es_texto_legible(datos_originales) else '⚠️  Verificar'}")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")

    def ejecutar_demo_completa(self):
        """Ejecuta la demostración completa"""
        print("🚨 DEMOSTRACIÓN MEJORADA - VERIFICACIÓN REAL DE CIFRADO")
        print("=" * 60)
        
        # Fase 1: Preparación
        print("\n1️⃣  PREPARANDO ARCHIVOS DE PRUEBA...")
        self.crear_archivos_prueba()
        
        input("\n⏸️  Presiona Enter para cifrado...")
        
        # Fase 2: Cifrado
        print("\n2️⃣  CIFRANDO ARCHIVOS...")
        self.cifrar_archivos_con_verificacion()
        
        # Fase 3: Demostración de ilegibilidad
        print("\n3️⃣  DEMOSTRANDO ILEGIBILIDAD...")
        self.demostrar_ilegibilidad()
        
        input("\n⏸️  Presiona Enter para recuperación...")
        
        # Fase 4: Recuperación
        print("\n4️⃣  RECUPERANDO ARCHIVOS...")
        self.descifrar_y_verificar()
        
        print("\n✅ DEMOSTRACIÓN COMPLETADA - CIFRADO VERIFICADO")

if __name__ == "__main__":
    demo = RansomwareDemoVerificacionReal()
    demo.ejecutar_demo_completa()
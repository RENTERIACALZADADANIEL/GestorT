import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("🔍 DIAGNÓSTICO DE CONEXIÓN")
print("=" * 50)

# 1. Verificar .env
print("\n1️⃣ Verificando .env...")
from dotenv import load_dotenv
load_dotenv()
print(f"   DB_HOST: {os.getenv('DB_HOST', 'NO ENCONTRADO')}")
print(f"   DB_USER: {os.getenv('DB_USER', 'NO ENCONTRADO')}")
print(f"   DB_NAME: {os.getenv('DB_NAME', 'NO ENCONTRADO')}")
print(f"   DB_PORT: {os.getenv('DB_PORT', 'NO ENCONTRADO')}")

# 2. Probar conexión
print("\n2️⃣ Probando conexión a MySQL...")
from src.models.database import Database
db = Database()
connection = db.connect()

if connection:
    print("   ✅ Conexión exitosa a MySQL")
    
    # 3. Verificar base de datos
    print("\n3️⃣ Verificando base de datos...")
    result = db.execute_query("SELECT DATABASE()")
    print(f"   BD actual: {result}")
    
    # 4. Verificar tablas
    print("\n4️⃣ Verificando tablas...")
    result = db.execute_query("SHOW TABLES")
    print(f"   Tablas encontradas: {result}")
    
    # 5. Verificar usuarios
    print("\n5️⃣ Verificando tabla usuarios...")
    result = db.execute_query("SELECT * FROM usuarios")
    if result:
        print(f"   ✅ {len(result)} usuario(s) encontrado(s):")
        for user in result:
            print(f"      - ID: {user['id']}, Username: {user['username']}, Rol: {user['rol']}")
            print(f"        Password: '{user['password']}'")
    else:
        print("   ❌ NO HAY USUARIOS en la tabla")
    
else:
    print("   ❌ Error de conexión a MySQL")
    print("   Verifica: XAMPP/WAMP encendido, credenciales en .env")

print("\n" + "=" * 50)
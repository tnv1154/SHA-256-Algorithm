import sqlite3
import os
import shutil

# Your MercyHacks keys
devDeviceId = "60bb114b-f6d7-4212-9365-37c241eac411"
machineId = "67d44e84e1ac220fb26baddc8ab20cff610cd6d9dca2a66b0256860d28d0e2ab"
macMachineId = "f746ffc339d6508d4dfedd05a6c1551d1a6c8a4ee378d42146a7064a49c0a736604f6ed9cd94789a306f8fcc0809445dfb54caf7a612832dca4e45401a7e413e"
sqmId = "{7B9EA628-C849-4BE7-B0EE-3D8F3086B60E}"

# Path to SQLite database
db_path = os.path.expandvars(r"%APPDATA%\Cursor\User\globalStorage\state.vscdb")

if os.path.exists(db_path):
    # Create backup
    backup_path = db_path + ".backup"
    shutil.copy2(db_path, backup_path)
    print(f"Created backup at {backup_path}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update values
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.devDeviceId'", (devDeviceId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.machineId'", (machineId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.macMachineId'", (macMachineId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'telemetry.sqmId'", (sqmId,))
    cursor.execute("UPDATE ItemTable SET value = ? WHERE key = 'storage.serviceMachineId'", (devDeviceId,))

    # Commit changes and close
    conn.commit()
    conn.close()
    print("Successfully updated Cursor database")
else:
    print(f"Database not found at {db_path}")
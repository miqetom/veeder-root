# tank_monitor.py (updated for decimal precision)
import telnetlib
import re
import struct
import csv
import datetime  # Added import

# Configuration (change to your IP address and port, your folder location, change tanks according to your needs)
IP = '192.168.0.7'
PORT = 10001
COMMAND = 'i201'
TANK = '00'
PENNINGTONTABLE_CSV = 'C:\\YOUR FOLDER\\YOURVEEDERROOTTABLE.csv'

PRODUCT_MAP = {
    '1': 'Regular E-10',
    '2': 'PREMIUM',
    '3': 'ON RD',
    '4': 'OFF RD',
    '5': 'DEF',
    '6': 'Conventional',

}

# ------------------- Telnet Fetching -------------------
def fetch_atg_data():
    try:
        tn = telnetlib.Telnet(IP, PORT)
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

    payload = bytes(COMMAND + TANK, 'utf-8')
    tn.write(b'\x01' + payload)
    tn.read_until(payload)
    data = tn.read_until(b'\x03', 10).replace(b'\x03', b'')
    tn.close()
    return data.decode('utf-8').strip()

# ------------------- Data Parsing -------------------
def ieee_to_float(hex_str):
    """Convert hex to float (no rounding)."""
    try:
        return struct.unpack('>f', bytes.fromhex(hex_str))[0]
    except:
        return 0.0  # Default to 0.0 on error

def ieee_to_rounded_float(hex_str, decimals=1):
    """Convert hex to float rounded to 1 decimal place."""
    f = ieee_to_float(hex_str)
    return round(f, decimals)

def parse_tank_data(response):
    if not response:
        return []
    
    data = response[10:]
    pattern = re.compile(r'(\d{2})(.)(\d{4})07([0-9A-Fa-f]{56})&{0,2}')
    tanks = []
    
    for match in pattern.finditer(data):
        tank_id, product, _, hex_fields = match.groups()
        hex_data = hex_fields[:56]
        fields = [hex_data[i:i+8] for i in range(0, 56, 8)]
        
        tank = {
            'Tank': tank_id,
            'Product': PRODUCT_MAP.get(product, 'UNKNOWN'),  # Mapped name
            'Volume': int(round(ieee_to_float(fields[0]))),  # Integer
            'TC Volume': int(round(ieee_to_float(fields[1]))),  # Integer
            'Ullage': int(round(ieee_to_float(fields[2]))),  # Integer
            'Height': ieee_to_rounded_float(fields[3]),      # 1 decimal
            'Water': ieee_to_rounded_float(fields[4]),       # 1 decimal
            'Temp': int(round(ieee_to_float(fields[5])))      # Integer
        }
        tanks.append(tank)
    
    return tanks

# ------------------- CSV Export -------------------
def write_csv(tanks, filename):
    if not tanks:
        print("No data to export.")
        return
    
    headers = ['Tank', 'Product', 'Volume', 'TC Volume', 'Ullage', 'Height', 'Water', 'Temp', 'Time']  # Added 'Time'
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for tank in tanks:
            # Format Height and Water to 1 decimal place explicitly
            tank['Height'] = f"{tank['Height']:.1f}"
            tank['Water'] = f"{tank['Water']:.1f}"
            writer.writerow(tank)
    print(f"CSV saved to {filename}")

# ------------------- Main -------------------
if __name__ == "__main__":
    response = fetch_atg_data()
    if not response:
        exit()
    
    tanks = parse_tank_data(response)
    # Capture current time and add to each tank
    capture_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for tank in tanks:
        tank['Time'] = capture_time
    write_csv(tanks, YOURVEEDERROOTTABLE_CSV)

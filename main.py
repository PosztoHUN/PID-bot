import discord
from discord.ext import commands, tasks
import aiohttp
import os
import json
from datetime import datetime

# =======================
# BEÁLLÍTÁSOK
# =======================
TOKEN = os.getenv("TOKEN")

PID_API_KEY = os.getenv("PID_API_KEY")
API_URL = "https://mapa.pid.cz/getData.php"

# =======================
# SEGÉDFÜGGVÉNYEK
# =======================
def is_kt8(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 9000 <= n <= 9110
    except:
        return False
    
def is_t1_nosztalgia(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 5001 <= n <= 5002
    except:
        return False
    
def is_t2_nosztalgia(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 6002 <= n <= 6004
    except:
        return False
    
def fill_tatra_t2r_nosztalgia():
    tatra_t2d_nosztalgia_numbers = [6003, 6004]
    return tatra_t2d_nosztalgia_numbers
    
def is_t3(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 5500 <= n <= 8799
    except:
        return False

def fill_tatra_t3m2_dvc():
    tatra_t3m2_dvc_numbers = [
        8009, 8015, 8051, 8053, 8063, 8067, 8068, 8072, 8074, 8076, 8077, 8079, 8080, 8082, 8083, 8087, 8088, 8089
    ]
    return tatra_t3m2_dvc_numbers

def fill_tatra_t3r_pv():
    tatra_t3r_pv_numbers = [
        8151, 8152, 8153, 8154, 8155, 8157, 8159, 8160, 8161, 8162, 8164, 8165, 8166, 8167, 8169, 8170, 8171, 8172, 8173, 8174, 8175, 8176, 8177, 8178, 8179, 8180, 8181, 8184, 8185
    ]
    return tatra_t3r_pv_numbers

def fill_tatra_t3r_p():
    tatra_t3r_p_numbers = [
        8214, 8215, 8216, 8217, 8222, 8224, 8227, 8232, 8234, 8235, 8236, 8237, 8239, 8240, 8241, 8243, 8300, 8301, 8304, 8305, 8308, 8309, 8313, 8314, 8315, 8316, 8317, 8318, 8319, 8320, 8323, 8324,
        8326, 8327, 8328, 8329, 8330, 8331, 8332, 8333, 8334, 8335, 8336, 8337, 8338, 8340, 8341, 8343,
        8345, 8346, 8347, 8348, 8349, 8350, 8352, 8353, 8354, 8355, 8356, 8357, 8358, 8359, 8360, 8361,
        8362, 8363, 8364, 8365, 8366, 8367, 8368, 8369, 8370, 8371, 8372, 8373, 8374, 8375, 8376, 8377,
        8378, 8379, 8380, 8381, 8382, 8383, 8384, 8385, 8386, 8387, 8388, 8389, 8390, 8391, 8392, 8393,
        8394, 8395, 8396, 8397, 8398, 8399, 8400, 8401, 8402, 8403, 8404, 8405, 8406, 8407, 8408, 8409,
        8410, 8411, 8412, 8413, 8414, 8415, 8416, 8417, 8418, 8419, 8421, 8423, 8424, 8425, 8426, 8427,
        8429, 8430, 8431, 8432, 8433, 8434, 8435, 8436, 8437, 8438, 8439, 8440, 8441, 8442, 8443, 8444,
        8445, 8446, 8447, 8448, 8449, 8450, 8451, 8452, 8453, 8454, 8455, 8456, 8457, 8458, 8459, 8460,
        8461, 8462, 8463, 8464, 8465, 8466, 8467, 8468, 8469, 8470, 8471, 8472, 8473, 8474, 8475, 8476, 8477,
        8478, 8479, 8480, 8481, 8482, 8483, 8484, 8485, 8486, 8487, 8488, 8489, 8490, 8491, 8492, 8493, 8494, 8495, 8496, 8497, 8498, 8499, 8500, 8501, 8502, 8503, 8504, 8505, 8506, 8507, 8508, 8509,
        8510, 8511, 8512, 8513, 8514, 8515, 8516, 8517, 8518, 8519, 8520, 8521, 8522, 8523, 8524, 8525, 8526, 8527, 8528, 8529, 8530, 8531, 8532, 8533, 8534, 8535, 8536, 8537, 8538, 8539, 8540, 8541,
        8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552, 8553, 8554, 8555, 8556, 8557, 8558, 8559, 8560, 8561, 8562, 8563, 8564, 8565, 8566, 8567, 8568, 8569, 8570, 8571, 8572,
        8573, 8574, 8575, 8576, 8577, 8578, 8579
    ]
    return tatra_t3r_p_numbers

def fill_tatra_t3r_plf():
    tatra_t3r_plf_numbers = [
        8251, 8252, 8253, 8254, 8255, 8256, 8257, 8258, 8259, 8260, 8261, 8262, 8263, 8264, 8265, 8266,
        8267, 8268, 8269, 8270, 8271, 8272, 8273, 8274, 8275, 8276, 8277, 8278, 8279, 8280, 8281, 8282,
        8283, 8284, 8285, 8286, 8287, 8288, 8289, 8290, 8291, 8292, 8293, 8294, 8295, 8296, 8297, 8298, 8299, 8751, 8752, 8753, 8754, 8755, 8756, 8757, 8758, 8759, 8760, 8761, 8762, 8763, 8764, 8765, 8766,
        8767, 8768, 8769, 8770, 8771, 8772, 8773, 8774, 8775, 8776, 8777, 8778, 8779, 8780
    ]
    return tatra_t3r_plf_numbers

def fill_tatra_t3_nosztalgia():
    tatra_t3_nosztalgia_numbers = [5602, 6102, 6149, 6339, 6340, 6892, 6921]
    return tatra_t3_nosztalgia_numbers

def fill_tatra_t3su_nosztalgia():
    tatra_t3su_nosztalgia_numbers = [7001, 7002]
    return tatra_t3su_nosztalgia_numbers

def fill_tatra_t3sucs_nosztalgia():
    tatra_t3sucs_nosztalgia_numbers = [7142, 7188, 7189, 7205, 7234, 7235, 7269, 7290, 7292]
    return tatra_t3sucs_nosztalgia_numbers

def fill_tatra_t3m_nosztalgia():
    tatra_t3m_nosztalgia_numbers = [8014, 8014, 8042, 8084, 8085]
    return tatra_t3m_nosztalgia_numbers

def is_t4_nosztalgia(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 5500 <= n <= 5501
    except:
        return False

def is_t6a5_nosztalgia(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 8601 <= n <= 8750
    except:
        return False
    
def is_k2_nosztalgia(vehicle_registration_number):
    try:
        n = int(vehicle_registration_number)
        return 6999 <= n <= 7000
    except:
        return False

# =======================
# DISCORD BOT INIT
# =======================
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


# =======================
# LOGGER LOOP (opcionális)
# =======================
@tasks.loop(seconds=30)
async def logger_loop():
    headers = {"X-Access-Token": PID_API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL, headers=headers, timeout=10) as r:
                if r.status != 200:
                    # print("Hiba a JSON lekéréskor:", r.status)  # <- ezt kikommentezheted
                    return
                data = await r.json()
        except Exception as e:
            # print("Hiba a JSON lekéréskor:", e)  # <- ezt is
            return

        features = data.get("features", [])
        if not features:
            # print("Nincs járműadat")  # <- törölheted
            return
        
# =======================
# KT8
# =======================
@bot.command()
async def pidkt8today(ctx, date: str = None):
    day = date or datetime.now().strftime("%Y-%m-%d")
    veh_dir = "logs/veh"
    kt8s = {}

    for fname in os.listdir(veh_dir):
        if not fname.endswith(".txt"):
            continue
        reg = fname.replace(".txt", "")
        if not is_kt8(reg):
            continue

        with open(os.path.join(veh_dir, fname), "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(day):
                    # Feltételezzük, hogy a log csak villamosokat tartalmaz
                    ts = line.split(" - ")[0]
                    trip_id = line.split("ID ")[1].split(" ")[0]
                    line_no = line.split("Vonal ")[1].split(" ")[0]
                    kt8s.setdefault(reg, []).append((ts, line_no, trip_id))

    if not kt8s:
        return await ctx.send(f"🚫 {day} napon nem közlekedett Tatra KT8D5R.N2P villamos.")

    out = [f"🚋 Tatra KT8D5R.N2P – forgalomban ({day})"]
    for reg in sorted(kt8s):
        first = min(kt8s[reg], key=lambda x: x[0])
        last = max(kt8s[reg], key=lambda x: x[0])
        out.append(f"{reg} — {first[0][11:16]} → {last[0][11:16]} (vonal {first[1]})")

    msg = "\n".join(out)
    for i in range(0, len(msg), 1900):
        await ctx.send(msg[i:i+1900])

# =======================

@bot.command()
async def pidkt8(ctx):
    active = {}
    headers = {"X-Access-Token": PID_API_KEY}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL, headers=headers, timeout=10) as r:
                if r.status != 200:
                    return
                data = await r.json()
        except:
            return

        for trip in data.get("trips", []):

            if trip.get("routeType") != 0:
                continue

            vehicle_label = str(trip.get("vehicle", "")).strip()
            if not vehicle_label.isdigit():
                continue

            num = int(vehicle_label)

            if not is_kt8(num):
                continue

            active[vehicle_label] = {
                "line": trip.get("route", "Ismeretlen"),
                "trip": trip.get("tripId", "Unknown"),
                "delay": trip.get("delay", 0)
            }

    if not active:
        return

    embed = discord.Embed(title="🚋 KT8 villamosok", color=0xff0000)

    for reg, info in sorted(active.items(), key=lambda x: int(x[0])):
        value = (
            f"Vonal: {info['line']}\n"
            f"Forgalmi: {info['trip']}\n"
            f"Késés: {info['delay']} mp"
        )

        if 9099 <= int(reg) <= 9110:
            value += "\n*🛠️ ex. Miskolc*"

        embed.add_field(name=reg, value=value, inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def pidt3today(ctx, date: str = None):
    day = date or datetime.now().strftime("%Y-%m-%d")
    veh_dir = "logs/veh"
    t3s = {}

    for fname in os.listdir(veh_dir):
        if not fname.endswith(".txt"):
            continue
        reg = fname.replace(".txt","")
        if not is_t3(reg):
            continue

        with open(os.path.join(veh_dir, fname), "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(day):
                    ts = line.split(" - ")[0]
                    trip_id = line.split("ID ")[1].split(" ")[0]
                    line_no = line.split("Vonal ")[1].split(" ")[0]
                    t3s.setdefault(reg, []).append((ts, line_no, trip_id))

    if not t3s:
        return await ctx.send(f"🚫 {day} napon nem közlekedett Tatra T3-as villamos.")

    out = [f"🚋 Tatra T3 – forgalomban ({day})"]
    for reg in sorted(t3s):
        first = min(t3s[reg], key=lambda x: x[0])
        last = max(t3s[reg], key=lambda x: x[0])
        out.append(f"{reg} — {first[0][11:16]} → {last[0][11:16]} (vonal {first[1]})")

    msg = "\n".join(out)
    for i in range(0, len(msg), 1900):
        await ctx.send(msg[i:i+1900])
        
#=======================

@bot.command()
async def pidt3(ctx):
    active = {}
    headers = {"X-Access-Token": PID_API_KEY}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL, headers=headers, timeout=10) as r:
                if r.status != 200:
                    return
                data = await r.json()
        except:
            return

        for trip in data.get("trips", []):

            if trip.get("routeType") != 0:
                continue

            vehicle_label = str(trip.get("vehicle", "")).strip()
            if not vehicle_label.isdigit():
                continue

            num = int(vehicle_label)

            if not is_t3(num):
                continue

            if num in fill_tatra_t3m2_dvc():
                subtype = "Tatra T3M2-DVC"
            elif num in fill_tatra_t3r_pv():
                subtype = "Tatra T3R.PV"
            elif num in fill_tatra_t3r_p():
                subtype = "Tatra T3R.P"
            elif num in fill_tatra_t3r_plf():
                subtype = "Tatra T3R.PLF"
            elif num in fill_tatra_t3_nosztalgia():
                subtype = "Tatra T3 *nosztalgia*"
            elif num in fill_tatra_t3sucs_nosztalgia():
                subtype = "Tatra T3SUCS *nosztalgia*"
            elif num in fill_tatra_t3m_nosztalgia():
                subtype = "Tatra T3M *nosztalgia*"
            elif num in fill_tatra_t3su_nosztalgia():
                subtype = "Tatra T3SU *nosztalgia*"
            else:
                subtype = "T3 (ismeretlen)"

            active[vehicle_label] = {
                "line": trip.get("route", "Ismeretlen"),
                "trip": trip.get("tripId", "Unknown"),
                "delay": trip.get("delay", 0),
                "subtype": subtype
            }

    if not active:
        return

    embed = discord.Embed(title="🚋 Tatra T3 villamosok", color=0xff0000)

    for reg, info in sorted(active.items(), key=lambda x: int(x[0])):
        value = (
            f"Altípus: {info['subtype']}\n"
            f"Vonal: {info['line']}\n"
            f"Forgalmi: {info['trip']}\n"
            f"Késés: {info['delay']} mp"
        )

        embed.add_field(name=reg, value=value, inline=False)

    await ctx.send(embed=embed)
        
@bot.command()
async def nosztalgia(ctx):
    active = {}
    headers = {"X-Access-Token": PID_API_KEY}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL, headers=headers, timeout=10) as r:
                if r.status != 200:
                    return
                data = await r.json()
        except:
            return

        for trip in data.get("trips", []):

            if trip.get("routeType") != 0:
                continue

            vehicle_label = str(trip.get("vehicle", "")).strip()
            if not vehicle_label.isdigit():
                continue

            num = int(vehicle_label)

            subtype = None

            if is_t1_nosztalgia(num):
                subtype = "Tatra T1 *nosztalgia*"
            elif is_t2_nosztalgia(num):
                subtype = "Tatra T2 *nosztalgia*"
            elif is_t4_nosztalgia(num):
                subtype = "Tatra T4 *nosztalgia*"
            elif is_t6a5_nosztalgia(num):
                subtype = "Tatra T6A5 *nosztalgia*"
            elif is_k2_nosztalgia(num):
                subtype = "Tatra K2 *nosztalgia*"
            elif num in fill_tatra_t3_nosztalgia():
                subtype = "Tatra T3 *nosztalgia*"
            elif num in fill_tatra_t3su_nosztalgia():
                subtype = "Tatra T3SU *nosztalgia*"
            elif num in fill_tatra_t3sucs_nosztalgia():
                subtype = "Tatra T3SUCS *nosztalgia*"
            elif num in fill_tatra_t3m_nosztalgia():
                subtype = "Tatra T3M *nosztalgia*"
            else:
                continue

            active[vehicle_label] = {
                "line": trip.get("route", "Ismeretlen"),
                "trip": trip.get("tripId", "Unknown"),
                "delay": trip.get("delay", 0),
                "subtype": subtype
            }

    if not active:
        return

    embed = discord.Embed(title="🚋 Nosztalgia Tatra villamosok", color=0xffa500)

    for reg, info in sorted(active.items(), key=lambda x: int(x[0])):
        value = (
            f"Altípus: {info['subtype']}\n"
            f"Vonal: {info['line']}\n"
            f"Forgalmi: {info['trip']}\n"
            f"Késés: {info['delay']} mp"
        )

        embed.add_field(name=reg, value=value, inline=False)

    await ctx.send(embed=embed)


# =======================
# BOT INDÍTÁS
# =======================
@bot.event
async def on_ready():
    print(f"Bot csatlakozva: {bot.user}")
    logger_loop.start()  # ha szeretnéd logolni is folyamatosan

bot.run(TOKEN)

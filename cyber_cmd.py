#!/usr/bin/env python3
import psutil
import time
import platform
import socket
import urllib.request
from urllib.error import URLError
from datetime import datetime
import random
from collections import deque

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.console import Console
from rich.prompt import Prompt

# --- THEME KONFIGURATION ---

THEMES = {
    "1": {"name": "Matrix", "main": "green", "warn": "yellow", "crit": "red", "accent": "cyan", "dim": "grey50"},
    "2": {"name": "Cyberpunk", "main": "bright_magenta", "warn": "yellow", "crit": "red", "accent": "bright_cyan", "dim": "grey50"},
    "3": {"name": "Ocean", "main": "blue", "warn": "yellow", "crit": "red", "accent": "bright_cyan", "dim": "grey50"},
    "4": {"name": "Fire", "main": "orange3", "warn": "bright_yellow", "crit": "bright_red", "accent": "yellow", "dim": "grey50"},
    "5": {"name": "Mono", "main": "white", "warn": "grey70", "crit": "red", "accent": "bright_white", "dim": "grey50"}
}

COLOR_MAIN = "green"
COLOR_WARN = "yellow"
COLOR_CRIT = "red"
COLOR_ACCENT = "cyan"
COLOR_DIM = "grey50"

def set_theme(choice):
    global COLOR_MAIN, COLOR_WARN, COLOR_CRIT, COLOR_ACCENT, COLOR_DIM
    if choice in THEMES:
        t = THEMES[choice]
        COLOR_MAIN = t["main"]
        COLOR_WARN = t["warn"]
        COLOR_CRIT = t["crit"]
        COLOR_ACCENT = t["accent"]
        COLOR_DIM = t["dim"]
        return t["name"]
    return "Matrix"

def get_color_by_percent(percent):
    if percent < 60: return COLOR_MAIN
    if percent < 85: return COLOR_WARN
    return COLOR_CRIT

# --- CACHED HELPER FUNKTIONEN ---

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1 (Offline)"

def get_public_ip():
    try:
        return urllib.request.urlopen('https://api.ipify.org', timeout=2).read().decode('utf8')
    except URLError:
        return "Offline/Error"

def get_cpu_name():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    return line.split(':')[1].strip().replace('(R)', '').replace('(TM)', '').replace(' CPU', '')
    except Exception:
        pass
    return platform.processor() or "UNKNOWN_PROCESSOR"

def generate_hacker_line():
    prefixes = ["[OK]", "[WARN]", "[INFO]", "[ERR]", "[*]", "[+]"]
    actions = [
        "Decrypting payload...", "Bypassing mainframe firewall...",
        "Injecting SQL chunk...", "Tracing proxy IP...",
        "Compiling kernel module...", "Cracking RSA-4096 key...",
        "Establishing secure tunnel...", "Dumping registry...",
        "Overriding system privileges..."
    ]
    ip = f"{random.randint(11,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    hex_val = f"0x{random.randint(0x1000, 0xFFFF):04X}"

    choices = [
        f"{random.choice(prefixes)} {random.choice(actions)}",
        f"Target node acquired: {ip}",
        f"Mem-Dump: {hex_val} 0x{random.randint(0x1000, 0xFFFF):04X}",
        f"Loading module {hex_val}.so ... SUCCESS",
        "".join(random.choices(["0", "1"], k=35)),
        f"Uplink to {ip}:ESTABLISHED."
    ]
    return random.choice(choices)

# --- MODULE ---

def generate_header():
    art = Text("=== [ CYBER COMMAND CENTER V3.0 - OPTIMIZED CORE ] ===", style=f"bold {COLOR_ACCENT}", justify="center")
    return Panel(art, box=box.MINIMAL, style=COLOR_MAIN)

def generate_sysinfo(local_ip, public_ip, cached_uname, cached_boot_time):
    table = Table(box=None, show_header=False, style=COLOR_MAIN)
    table.add_column("Key", style=f"bold {COLOR_ACCENT}")
    table.add_column("Value")

    # Nutzt den übergebenen Boot-Time Cache, spart CPU
    uptime = datetime.now() - cached_boot_time
    uptime_str = str(uptime).split('.')[0]

    table.add_row("OS:", f"{cached_uname.system} {cached_uname.release}")
    table.add_row("Node:", cached_uname.node)
    table.add_row("Uptime:", uptime_str)
    table.add_row("Local IP:", local_ip)
    table.add_row("Pub IP:", public_ip)

    return Panel(table, title="[ SYS INFO ]", border_style=COLOR_MAIN)

def generate_hardware(blink_state, cpu_name):
    table = Table(box=None, show_header=False, expand=True)
    table.add_column("Res", style=f"bold {COLOR_ACCENT}", width=6)
    table.add_column("Bar", ratio=1)
    table.add_column("Val", justify="right", width=7)

    def make_circle_bar(percent, color):
        total_circles = 30
        filled = int((percent / 100) * total_circles)
        return Text("●" * filled + "○" * (total_circles - filled), style=color)

    cpu = psutil.cpu_percent(interval=None)
    cpu_col = get_color_by_percent(cpu)

    table.add_row("CHIP", Text(cpu_name, style=COLOR_DIM), "")
    table.add_row("LOAD", make_circle_bar(cpu, cpu_col), Text(f"{cpu}%", style=cpu_col))
    table.add_row("", "", "")

    ram = psutil.virtual_memory()
    ram_col = get_color_by_percent(ram.percent)
    table.add_row("MEM", make_circle_bar(ram.percent, ram_col), Text(f"{ram.percent}%", style=ram_col))

    border = COLOR_CRIT if (cpu > 90 or ram.percent > 90) and blink_state else COLOR_MAIN
    return Panel(table, title="[ HARDWARE LOAD ]", border_style=border)

def generate_disk():
    table = Table(box=None, show_header=False, expand=True)
    table.add_column("Dev", style=f"bold {COLOR_ACCENT}")
    table.add_column("Usage", style=COLOR_MAIN)
    table.add_column("Free", justify="right")

    usage = psutil.disk_usage('/')
    u_col = get_color_by_percent(usage.percent)

    total_circles = 30
    filled = int((usage.percent / 100) * total_circles)
    bar_text = "●" * filled + "○" * (total_circles - filled)

    table.add_row("/", Text(bar_text, style=u_col), f"{usage.free / (1024**3):.1f} GB")

    return Panel(table, title="[ DISK I/O ]", border_style=COLOR_MAIN)

def generate_network(net_start, start_time):
    net_now = psutil.net_io_counters()
    td = time.time() - start_time
    if td == 0: td = 1 # Fallback, um ZeroDivision zu vermeiden

    tx_bps = (net_now.bytes_sent - net_start.bytes_sent) / td
    rx_bps = (net_now.bytes_recv - net_start.bytes_recv) / td

    table = Table(box=None, show_header=False)
    table.add_column("Type", style=f"bold {COLOR_ACCENT}")
    table.add_column("Speed", style=COLOR_MAIN)
    table.add_column("Total", justify="right")

    table.add_row("TX Up:", f"{tx_bps / 1024 / 1024:.2f} MB/s", f"{net_now.bytes_sent / (1024**3):.2f} GB")
    table.add_row("RX Dn:", f"{rx_bps / 1024 / 1024:.2f} MB/s", f"{net_now.bytes_recv / (1024**3):.2f} GB")

    return Panel(table, title="[ NET TRAFFIC ]", border_style=COLOR_MAIN)

def generate_processes():
    table = Table(box=box.SIMPLE, style=COLOR_MAIN, expand=True)
    table.add_column("PID", style=COLOR_ACCENT)
    table.add_column("NAME")
    table.add_column("CPU%", justify="right")
    table.add_column("MEM%", justify="right")

    procs = []
    # Die ressourcenintensivste Funktion im Skript (wird nun per Throttling seltener aufgerufen)
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try: procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): pass

    procs = sorted(procs, key=lambda p: p.get('cpu_percent') or 0, reverse=True)

    for p in procs[:8]:
        cpu, mem = p.get('cpu_percent', 0), p.get('memory_percent', 0)
        table.add_row(str(p['pid']), p['name'][:10], f"{cpu:.1f}", f"{mem:.1f}")

    return Panel(table, title="[ TOP PROCESSES ]", border_style=COLOR_MAIN)

def generate_fake_terminal(log_queue):
    text = Text("\n".join(log_queue), style=COLOR_DIM)
    return Panel(text, title="[ TERMINAL UPLINK / DEMO ]", border_style=COLOR_MAIN)

def generate_matrix_rain():
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ§$%&/()=?"
    text = Text()

    # Leicht optimierte Schleife für weniger String-Overhead
    for i in range(8):
        line = []
        for j in range(40):
            if random.random() > 0.4:
                style = random.choice([COLOR_MAIN, COLOR_ACCENT, COLOR_DIM, "white"])
                text.append(random.choice(chars), style=style)
            else:
                text.append(" ")
        if i < 7:
            text.append("\n")

    return Panel(text, title="[ NEUROMANCER STREAM ]", border_style=COLOR_MAIN)

# --- LAYOUT ENGINE ---

def make_layout() -> Layout:
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    )
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="sysinfo", size=8),
        Layout(name="hardware", size=7),
        Layout(name="disk", size=6),
        Layout(name="matrix_rain")
    )
    layout["right"].split_column(
        Layout(name="network", size=6),
        Layout(name="processes", size=11),
        Layout(name="fake_term")
    )
    return layout

# --- BOOT SEQUENZ & MAIN LOOP ---

def interactive_boot():
    console = Console()
    console.clear()

    console.print(Panel("INITIALIZING CYBER COMMAND BOOT SEQUENCE...", style="bold cyan", expand=False))
    console.print("\n[bold white]Verfügbare Uplink-Themes:[/bold white]")

    for key, data in THEMES.items():
        console.print(f"[[bold cyan]{key}[/bold cyan]] {data['name']} (Primary: {data['main']})", style=data['main'])

    console.print()

    choice = Prompt.ask("[bold white]Bitte Core-System-Theme wählen[/bold white]", choices=list(THEMES.keys()), default="1")
    theme_name = set_theme(choice)

    console.print(f"\n[bold green][*] Theme '{theme_name}' geladen.[/bold green]")
    console.print("[*] Etabliere Netzwerk-Uplink und lade Cache (Bitte warten)...")

def main():
    interactive_boot()

    # -- CACHING (Einmaliges Laden schwerer Daten) --
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    cpu_name = get_cpu_name()
    cached_uname = platform.uname()
    cached_boot_time = datetime.fromtimestamp(psutil.boot_time())

    layout = make_layout()
    net_start = psutil.net_io_counters()
    start_time = time.time()

    # Initiale Renderings erzwingen, damit keine leeren Panels beim Start existieren
    layout["disk"].update(generate_disk())
    layout["processes"].update(generate_processes())

    psutil.cpu_percent(interval=0.1)

    blink_state = False
    fake_logs = deque(maxlen=10)
    tick = 0 # Frame-Counter für Performance-Throttling

    try:
        with Live(layout, refresh_per_second=2, screen=True) as live:
            while True:
                blink_state = not blink_state
                tick += 1

                # Füllt das Fake-Terminal
                for _ in range(random.randint(1, 2)):
                    fake_logs.append(generate_hacker_line())

                # --- FAST UPDATES (Jeder Tick / 0.5s) ---
                layout["header"].update(generate_header())
                layout["sysinfo"].update(generate_sysinfo(local_ip, public_ip, cached_uname, cached_boot_time))
                layout["hardware"].update(generate_hardware(blink_state, cpu_name))
                layout["network"].update(generate_network(net_start, start_time))
                layout["fake_term"].update(generate_fake_terminal(fake_logs))
                layout["matrix_rain"].update(generate_matrix_rain())

                # --- THROTTLED UPDATES (Resourcen schonen) ---
                if tick % 4 == 0: # Alle 2 Sekunden (4 Ticks)
                    layout["processes"].update(generate_processes())

                if tick % 20 == 0: # Alle 10 Sekunden (20 Ticks)
                    layout["disk"].update(generate_disk())

                # Timer Reset für Netzwerk
                net_start = psutil.net_io_counters()
                start_time = time.time()

                time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[!] Command Center offline.")

if __name__ == "__main__":
    main()

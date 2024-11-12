from datetime import datetime
from bluepy.btle import Scanner

log_file = "scanner_results.txt"
actual_time = datetime.now()
format_time = actual_time.strftime("%Y-%m-%d %H:%M:%S")


def add_entry_to_file(filename, message):
    with open(filename, "a") as file:
        file.write(message)
        file.flush()


def find_device_by_mac(target_mac):
    scanner = Scanner()
    devices = scanner.scan(10.0)  # Scanning for 10 seconds
    
    found = False  # Flaga, która śledzi, czy urządzenie zostało znalezione

    for dev in devices:
        print(f"Znaleziono urządzenie: {dev.addr}")  # Print to console

        # Check if the found device matches the target MAC address
        if dev.addr.lower() == target_mac.lower():
            found_message = f"Urządzenie o adresie MAC {target_mac} zostało znalezione!\n"
            print(found_message, end="")
            status_message = "true\n"
            write_message = format_time + ";" + status_message
            add_entry_to_file(log_file, write_message)
            found = True  # Ustaw flagę na True, jeśli urządzenie zostało znalezione
            break  # Exit loop if device is found

    # Jeśli urządzenie nie zostało znalezione, wpisz odpowiednią wiadomość do pliku
    if not found:
        not_found_message = f"Urządzenie o adresie MAC {target_mac} nie zostało znalezione.\n"
        print(not_found_message, end="")
        status_message = "false\n"
        write_message = format_time + ";" + status_message
        add_entry_to_file(log_file, write_message)


# Example usage
target_mac = "EE:EE:EE:EE:EE:EE"  # Replace with the target BLE MAC address
find_device_by_mac(target_mac)


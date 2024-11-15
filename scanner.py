from datetime import datetime
from bluepy.btle import Scanner

log_file = "scanner_results.txt"

def get_current_time_formatted():
    # Get the current time formatted as a string.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add_entry_to_file(filename, message):
    with open(filename, "a") as file:
        file.write(message)
        file.flush()

def scan_devices(scan_time=10.0):
    # Scan for devices for a specified duration.
    scanner = Scanner()
    return scanner.scan(scan_time)

def check_device_by_mac(target_mac, devices, log_file):
    # Check if a device with the target MAC address is in the scanned devices and log the result.
    found = False

    for dev in devices:
        print(f"Found device: {dev.addr}")

        if dev.addr.lower() == target_mac.lower():
            found_message = f"Device with MAC address {target_mac} found!\n"
            print(found_message, end="")
            status_message = "true\n"
            write_message = f"{get_current_time_formatted()};{status_message}"
            add_entry_to_file(log_file, write_message)
            found = True
            break

    if not found:
        not_found_message = f"Device with MAC address {target_mac} not found.\n"
        print(not_found_message, end="")
        status_message = "false\n"
        write_message = f"{get_current_time_formatted()};{status_message}"
        add_entry_to_file(log_file, write_message)


# Example usage
target_mac = "FF:FF:FF:FF:FF:FF"  # Replace with the target BLE MAC address
devices = scan_devices()
check_device_by_mac(target_mac, devices, log_file)


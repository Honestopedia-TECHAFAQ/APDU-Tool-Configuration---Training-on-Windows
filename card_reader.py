import smartcard
from smartcard.System import readers
from smartcard.util import toHexString
import logging

logging.basicConfig(
    filename="cosmo_x_interaction.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

AID_APPLET = [0xA0, 0x00, 0x00, 0x77, 0x03, 0x0C, 0x60, 0x00, 0x00, 0x00, 0xFE, 0x00, 0x00, 0x05, 0x00, 0x00]

def send_apdu_command(reader, apdu_command, description=""):
    try:
        connection = reader.createConnection()
        connection.connect()
        logging.info(f"{description}: Sending APDU: {toHexString(apdu_command)}")

        response, sw1, sw2 = connection.transmit(apdu_command)
        logging.info(f"{description}: Response: {toHexString(response)}, SW1: {sw1}, SW2: {sw2}")

        if sw1 == 0x90 and sw2 == 0x00:
            logging.info(f"{description}: Success.")
        else:
            logging.warning(f"{description}: Failure. SW1={sw1}, SW2={sw2}")

        return response, sw1, sw2
    except Exception as e:
        logging.error(f"Error during {description}: {e}")
        return None, None, None

def select_aid(reader):
    apdu_select_aid = [0x00, 0xA4, 0x04, 0x00, len(AID_APPLET)] + AID_APPLET
    return send_apdu_command(reader, apdu_select_aid, "Selecting AID")

def initialize_keys(reader, pin, puk, so_key):
    logging.info("Initializing keys...")
    apdu_set_pin = [0x00, 0x20, 0x00, 0x00, len(pin)] + pin
    send_apdu_command(reader, apdu_set_pin, "Setting PIN")
    
    apdu_set_puk = [0x00, 0x21, 0x00, 0x00, len(puk)] + puk
    send_apdu_command(reader, apdu_set_puk, "Setting PUK")
    
    apdu_set_so_key = [0x00, 0x22, 0x00, 0x00, len(so_key)] + so_key
    send_apdu_command(reader, apdu_set_so_key, "Setting SO Key")

def generate_rsa_key(reader):
    logging.info("Generating RSA Key Pair...")
    apdu_gen_rsa = [0x00, 0x47, 0x00, 0x00, 0x30]
    return send_apdu_command(reader, apdu_gen_rsa, "Generating RSA Key")

def generate_ecdsa_key(reader):
    logging.info("Generating ECDSA Key Pair...")
    apdu_gen_ecdsa = [0x00, 0x48, 0x00, 0x00, 0x20]
    return send_apdu_command(reader, apdu_gen_ecdsa, "Generating ECDSA Key")

def generate_csr(reader, key_ref, csr_template):
    logging.info(f"Generating CSR using key reference {key_ref}...")
    apdu_csr = [0x00, 0x50, key_ref, 0x00, len(csr_template)] + csr_template
    return send_apdu_command(reader, apdu_csr, "Generating CSR")

def import_certificate(reader, cert_data):
    logging.info("Importing Certificate...")
    apdu_import_cert = [0x00, 0xD6, 0x00, 0x00, len(cert_data)] + cert_data
    return send_apdu_command(reader, apdu_import_cert, "Importing Certificate")

def rename_certificate(reader, key_id, alias):
    logging.info(f"Renaming Certificate (Key ID: {key_id})...")
    apdu_rename = [0x00, 0x24, key_id, 0x00, len(alias)] + alias
    return send_apdu_command(reader, apdu_rename, "Renaming Certificate")

def unblock_and_set_pin(reader, puk, new_pin):
    logging.info("Unblocking PIN and setting a new PIN...")
    apdu_unblock_pin = [0x00, 0x2C, 0x00, 0x00, len(puk) + len(new_pin)] + puk + new_pin
    return send_apdu_command(reader, apdu_unblock_pin, "Unblocking PIN and Setting New PIN")

def change_pin(reader, old_pin, new_pin):
    logging.info("Changing PIN...")
    apdu_change_pin = [0x00, 0x24, 0x00, 0x00, len(old_pin) + len(new_pin)] + old_pin + new_pin
    return send_apdu_command(reader, apdu_change_pin, "Changing PIN")

def delete_key(reader, key_id):
    logging.info(f"Deleting Key with Key ID: {key_id}...")
    apdu_delete_key = [0x00, 0x46, key_id, 0x00, 0x00]
    return send_apdu_command(reader, apdu_delete_key, "Deleting Key")

def main():
    available_readers = readers()
    if not available_readers:
        logging.error("No smart card readers detected. Exiting.")
        return

    reader = available_readers[0]
    logging.info(f"Using reader: {reader}")

    if select_aid(reader) is None:
        logging.error("Failed to select AID. Exiting.")
        return

    initialize_keys(reader, [0x12, 0x34], [0x56, 0x78, 0x90, 0x12, 0x34], [0x00] * 24)
    generate_rsa_key(reader)
    generate_ecdsa_key(reader)
    unblock_and_set_pin(reader, [0x56, 0x78, 0x90], [0x12, 0x34])
    change_pin(reader, [0x12, 0x34], [0xAB, 0xCD])

    dummy_cert = [0x30, 0x82, 0x01, 0x0A]  
    import_certificate(reader, dummy_cert)

    rename_certificate(reader, 0x01, [0x41, 0x6C, 0x69, 0x61, 0x73])  

if __name__ == "__main__":
    main()

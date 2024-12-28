### 2. **Specific Command Calls**

The script contains multiple functions, and if you want to trigger any specific action separately, you can modify the `main()` function or directly call these functions. Here are commands based on specific tasks:

#### **Select AID Command:**

To select the AID from the smart card reader:

`python -c "from card_reader import readers, select_aid; reader = readers()[0]; select_aid(reader)"
`


#### **Initialize Keys (PIN, PUK, SO):**

To initialize the keys (PIN, PUK, SO):

`python -c "from card_reader import readers, initialize_keys; reader = readers()[0]; initialize_keys(reader, [0x12, 0x34], [0x56, 0x78, 0x90, 0x12, 0x34], [0x00] * 24)"
`


#### **Generate RSA Key Pair:**

To generate an RSA key pair:

`python -c "from card_reader import readers, generate_rsa_key; reader = readers()[0]; generate_rsa_key(reader)"
`


#### **Generate ECDSA Key Pair:**

To generate an ECDSA key pair:

`python -c "from card_reader import readers, generate_ecdsa_key; reader = readers()[0]; generate_ecdsa_key(reader)"
`


#### **Unblock PIN and Set New PIN:**

To unblock the PIN and set a new PIN:

`python -c "from card_reader import readers, unblock_and_set_pin; reader = readers()[0]; unblock_and_set_pin(reader, [0x56, 0x78, 0x90], [0x12, 0x34])"
`


#### **Change PIN:**

To change the PIN:

`python -c "from card_reader import readers, change_pin; reader = readers()[0]; change_pin(reader, [0x12, 0x34], [0xAB, 0xCD])"
`


#### **Import Certificate:**

To import a certificate:

`python -c "from card_reader import readers, import_certificate; reader = readers()[0]; import_certificate(reader, [0x30, 0x82, 0x01, 0x0A])"
`


#### **Rename Certificate:**

To rename a certificate:

`python -c "from card_reader import readers, rename_certificate; reader = readers()[0]; rename_certificate(reader, 0x01, [0x41, 0x6C, 0x69, 0x61, 0x73])"
`


### . **Check Log File for Results**

After running any of these commands, you can check the log file (`cosmo_x_interaction.log`) for detailed results:

cat cosmo_x_interaction.log

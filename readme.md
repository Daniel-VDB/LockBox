# LOCKBOX
#### Video Demo:  https://youtu.be/E2xIDsTKh74
#### Description:

Lockbox is an all purpose safety app, specialising in 
lossless file compression and password-based encryption, 
aimed at protecting and preparing files for cloud storage.

(**please read the disclaimer below before using**)

Lockbox makes use of the ZSTD lossless compression and AES
encryption algorithms in order to create file archives 
which are secure and safe for cloud storage, minimising
risk and decreasing storage costs.

Lockbox's can encrypt and decrypt any file type,
however compression efficiency varies depending on file structure

File types ranked by compression efficiency:
1. .txt, .csv, .json, .xml (Highly effective)
2. .docx, .xlsx, .pdf (moderately effective)
3. .exe, .dll (minimal effect)
4. .jpg, .png, .mp4, .zip (little to no compression)

Encryption algorithms are written in C, and UI is designed
through tkinter. Passwords are stored locally on an sqlite3 database file

Lockbox also has a password storage feature to facilitate the managing of 
file passwords. It allows for locally storing password details such as:
1. The service name (Mandatory, Which service the password pertains to (I.E "LockBox"))
2. Username (Mandatory, could be a file name as well)
3. Email (Optional)
4. password (Mandatory)
5. Additional notes (optional)

## DISCLAIMER

This software is provided “as is” and without any warranty.
By using this software, you acknowledge that:

The author(s) are not responsible for any loss of data, files, or other damage resulting from its use.

You use the software at your own risk. <------------------

It is recommended to backup your files before compression or decompression.

There is no guarantee that the software will work correctly with all file types or systems.

The author(s) disclaim all warranties, including, but not limited to:

Merchantability

Fitness for a particular purpose

Non-infringement

Under no circumstances shall the author(s) be liable for:

Direct, indirect, incidental, special, or consequential damages

Loss of data or profits

Any other claims arising from the use of this software

## Usage instructions

---- Encoding/decoding files ----
1. Navigate to the "file compression" screen

2. Select files for encoding/decoding

3. Toggle the proper mode (using button 
in the second UI box)

4. Enter the encryption key (the key you would 
like to use to decrypt files later on. It is best
practice to store this password in the passwords screen
or otherwise)

5. Press "Compress and encrypt" or "Restore", and select the desired location
to store the results


---- Creating passwords ----
1. Navigate to the "passwords" screen

2. Click "Add new password"

3. Fill in the required fields, as well as additional notes 
related to the password

4. Click "Save"

Your password will now be stored and can be found by going to the
"passwords" menu, highlighting the correct password and then clicking
"show password".

---- Editing a password ----
1. Navigate to the "passwords" screen

2. Highlight desired password

3. Click "Edit password"

4. Make desired changes

5. Click "Save"

---- Deleting a password
1. Navigate to the "passwords" screen

2. Highlight desired password

3. Click "Delete password"

4. Click "Confirm"

## License

This project includes Zstandard (Zstd) code:

- Copyright (c) 2016-2024, Facebook, Inc.
- Licensed under the BSD 2-Clause License. See LICENSE.txt file for details. (scripts/c_scripts/LISCENCE.TXT)
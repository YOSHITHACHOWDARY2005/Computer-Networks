from ftplib import FTP

ftp = FTP("ftp.dlptest.com")
ftp.login(user="dlpuser", passwd="rNrKYTX9g7z3RgJRmxWuGHbeu")

print("Directory listing:")
ftp.retrlines("LIST")

# Upload
with open("test.txt", "w") as f:
    f.write("Hello FTP!")

with open("test.txt", "rb") as f:
    ftp.storbinary("STOR test.txt", f)
print("Uploaded test.txt")

# Download
with open("downloaded.txt", "wb") as f:
    ftp.retrbinary("RETR test.txt", f.write)
print("Downloaded test.txt")

ftp.quit()

import sys
sys.exit(0)

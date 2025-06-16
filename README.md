# veeder-root
A simple python script to poll an IP based Gilbarco Veeder-Root tank monitor and export as a CSV file. Tested and working on TLS-300, TLS-350, TLS-400, TLS-400+. You will need either an IP card installed and configured, or a serial to ethernet adapter. This only works on Python v3.12, as telnet is no longer supported as of 3.13. 

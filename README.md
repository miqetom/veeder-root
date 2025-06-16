# veeder-root
A simple python script to poll an IP based Gilbarco Veeder-Root tank monitor and export as a CSV file. Tested and working on TLS-300, TLS-350, TLS-400, TLS-400+. 
Under configuration change the IP address and port to point to the VR, as well as the folder destination for the CSV. 

You will need either an IP card installed and configured, or a serial to ethernet adapter. 

This only works on Python v3.12, as telnet is no longer supported as of 3.13. 

Please note that the TIME function isn't pulling the actual time from the Veeder Root, as these can be programmed incorrectly. The time output is the time of capture. 

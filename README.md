# ftp_attack
    Before running the code, you need to have a target FTP server that you want to attack. The FTP server can be on your local network or on the Internet. You should have the IP address or hostname of the server ready.

    You also need to have a redirection page ready. This is the page that you will inject with malicious code to redirect users to a phishing site or some other malicious destination. You can create a simple HTML page with a script tag that redirects to the desired URL. Save the page in a file (e.g., malicious.html) on your local machine.

    Optional: If you want to perform a brute-force attack on the FTP server, you need to have a list of username and password combinations in a text file. Each line of the file should have the format username:password. You can use a tool like Hydra to generate such a file.

    Open a terminal or command prompt on your local machine, navigate to the directory where you saved the ftp_attack.py file and run the script using Python 3. Make sure you have the ftplib and optparse modules installed.

    Use the following command-line arguments to run the script:

php

python ftp_attack.py -H <target_host> -r <redirection_page> [-f <userpass_file>]

Replace <target_host> with the IP address or hostname of the FTP server you want to attack. If you want to attack multiple servers, separate their IP addresses or hostnames with commas and spaces.

Replace <redirection_page> with the path to the redirection page you created earlier (e.g., ./malicious.html).

If you want to perform a brute-force attack, add the optional -f argument followed by the path to the user/password file (e.g., -f ./userpass.txt).

    Press Enter to run the script. The script will try to log in to the FTP server using anonymous login first. If that fails, it will try to log in using the credentials from the user/password file (if provided). If it finds valid credentials, it will download the default pages from the FTP server, inject the malicious code into them and upload them back to the server.

    Check the FTP server to see if the injected code is working as intended. If everything works correctly, users who access the default pages on the server will be redirected to the phishing or malicious site.

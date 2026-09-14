import re
from subprocess import run
from apicall import check_api_IP
from difflib import SequenceMatcher


def checkSPF(msg):
    """
    checker les données spf dans le mail
    """
    result = False
    spf = msg.get('Received-SPF')
    print(f"SPF result: {spf}")

    if not spf:
        print("Le message n'est pas spf")
    else:
        matche = re.findall(r'\bpass\b', spf, re.IGNORECASE)
        if matche:
            domain = re.search(r'domain of \S+@([\w.-]+)', spf, re.IGNORECASE)
            ipdomain = re.search(r'client-ip=([\d.]+)', spf, re.IGNORECASE)
            domainISP = re.findall(r'include:([^\s"]+)', run(["nslookup", "-type=TXT", domain.group(1)], capture_output=True, text=True).stdout.strip())
            print(f"Le message est spf, domaine: {domain.group(1)}, ip: {ipdomain.group(1)}, domaine ISP: {domainISP}")
            Api_res = check_api_IP(ipdomain.group(1))
            print(f"API result: {Api_res}")
        else:
            print("Le message n'est pas spf")
            result = False
    return result




def normalize(s):
    """Reduit un nom d'ISP ou un domaine a une forme comparable."""
    s = s.lower()
    s = re.sub(r'\.(com|net|org|io|fr|co\.uk)$', '', s)
    s = re.sub(r'\b(inc|llc|ltd|corp|corporation|co|sa|sas|sarl|gmbh|bv|plc)\b', '', s)
    return re.sub(r'[^a-z0-9]', '', s)


def compare_result(API_result, domain_ISP):
    """
    compare les resultats de l'api et le domaine de l'ISP
    """
    if not API_result or "data" not in API_result:
        print("Pas de reponse API exploitable")
        return False

    data = API_result["data"]
    refs = [data.get("isp", ""), data.get("domain", "")] + data.get("hostnames", [])
    refs = [normalize(r) for r in refs if r]

    for inc in domain_ISP:
        n = normalize(inc)
        for r in refs:
            if n == r or n in r or r in n or SequenceMatcher(None, n, r).ratio() > 0.8:
                print(f"Correspondance: {inc} <-> {data.get('isp')}")
                return True

    print(f"Aucune correspondance: {domain_ISP} vs {data.get('isp')} / {data.get('domain')}")
    return False
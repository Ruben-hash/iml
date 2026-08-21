import re
from subprocess import run
from apicall import check_api_IP


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
            Api_ip = check_api_IP(ipdomain.group(1))
            result = True
        else:
            print("Le message n'est pas spf")
            result = False
    return result


def compare_result(API_result, domain_ISP):
    """
    compare les resultats de l'api et le domaine de l'ISP
    """

import re

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
            domain = re.search(r'@([^\s]+)', spf, re.IGNORECASE)
            print(f"Le message est spf et le domaine est: {domain.group(1)}")
            ipdomain = re.search(r'client-ip=([^\s]+)', spf, re.IGNORECASE)
            print(f"Le message est spf et l'ip est: {ipdomain.group(1)}")
        result = True
    return result


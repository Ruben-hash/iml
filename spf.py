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
        matches = re.findall(r'\bpass\b', spf, re.IGNORECASE)
        print(f"matches: {matches}")
        result = True
    return result


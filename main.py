from email import policy
from email.parser import BytesParser
from spf import checkSPF

score = 10

def mail(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return msg


def main():
    f = "test.eml"
    msg = mail(f)
    rep= checkSPF(msg)
    print(f"SPF result: {rep}")

if __name__ == "__main__":
    main()
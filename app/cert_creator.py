from socket import gethostname

from OpenSSL import crypto

CERT_FILE = "client.cert"
KEY_FILE = "client.key"


def create_self_signed_cert():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)
    cert = crypto.X509()
    cert.get_subject().C = "PL"
    cert.get_subject().ST = "Lublin"
    cert.get_subject().L = "Lublin"
    cert.get_subject().O = "ProjektPAS"
    cert.get_subject().OU = "PP"
    cert.get_subject().CN = "localhost"
    print(gethostname())
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    open(CERT_FILE, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8")
    )
    open(KEY_FILE, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8")
    )

create_self_signed_cert()
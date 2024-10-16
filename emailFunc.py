import binascii
import imaplib
import email
import os
import base64
import nntplib
import config



mail_pass = config.mail_tok
gmail = config.gmail
# mail_pass = ""
# gmail = ""
# mail_pass = gmail
# gmail = imap
imap_server = "imap.gmail.com"


imap = imaplib.IMAP4_SSL(imap_server)
imap.login(gmail, mail_pass)
imap.select("INBOX")


filenames = []
counter = 1
def get_files(number):
    global from_who,title,letter
    global counter
    res, msg = imap.fetch(number, '(RFC822)')

    msg = email.message_from_bytes(msg[0][1])
    from_who = nntplib.decode_header(msg["From"])
    title = nntplib.decode_header(msg["Subject"])
    for part in msg.walk():
        if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
            try:
                letter = base64.b64decode(part.get_payload()).decode()
            except binascii.Error:
                letter = part.get_payload()

    for part in msg.walk():
        if part.get_filename() == None:
            continue
        else:
            filename = part.get_filename()
            filename = str(email.header.make_header(email.header.decode_header(filename)))

            fp = open(os.path.join("documents/", str(counter)+filename), 'wb')
            counter+=1
            fp.write(part.get_payload(decode=1))
            fp.close
            filenames.append(str(counter - 1) + filename)



def save_all_file():

    emails = imap.search(None, 'UNSEEN')
    emails = (b" ".join(list(emails)[1])).split()
    for i in emails:
        get_files(i)

save_all_file()
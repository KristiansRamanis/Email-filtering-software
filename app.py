import mysql.connector
import re


# Pieslēdzas datubāzei
def connect_to_database():

    try:
        conn = mysql.connector.connect(
            host="78.84.210.187",
            port=8086,
            user="username",
            password="password",
            database="Email"
        )
        return conn
    except mysql.connector.Error as err:
        print("Kļūda, nevarēja pieslēgties datubāzei:", err)
        return None

# Iegūst e-pastus no datubāzes
def fetch_emails_from_database(connection):

    if connection is None:
        print("Nevar iegūt e-pastus, jo nav iespējams pieslēgties datubāzei.")
        return []
    else:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT Subject, Body FROM Epasti")
            emails = cursor.fetchall()
            cursor.close()
            return emails
        except mysql.connector.Error as err:
            print("Kļūda, nevarēja iegūt datus no datubāzes:", err)
            cursor.close()
            return []
        
# Apstrādā e-pastus un identificē atslēgvārdus, veic filtrēšanu
def process_emails(emails):

    keywords_regex_svarigi = re.compile(r'\b(?:Svarīgs|Svarīgi|Svarīga)\b', re.IGNORECASE)
    keywords_regex_jautajumi = re.compile(r'\b(?:Kā|Vai|Kādas|Kuras|Kāpēc)\b', re.IGNORECASE)

    svarigi_emails = []
    jautajumi_emails = []
    nenosakamie_emails = []

    for subject, body in emails:
        if keywords_regex_svarigi.search(subject) or keywords_regex_svarigi.search(body):
            svarigi_emails.append((subject, body))
        elif keywords_regex_jautajumi.search(subject) or keywords_regex_jautajumi.search(body):
            jautajumi_emails.append((subject, body))
        else:
            nenosakamie_emails.append((subject, body))

    return svarigi_emails, jautajumi_emails, nenosakamie_emails

# Izvada rezultātus
def print_results(svarigi_emails, jautajumi_emails, nenosakamie_emails):
    print("Grupa 'Svarīgi':")
    for email in svarigi_emails:
        print(email)
    print("Grupa 'Jautājumi':")
    for email in jautajumi_emails:
        print(email)
    print("Grupa 'Nenosakāmie':")
    for email in nenosakamie_emails:
        print(email)


# Galvenā programmas funkcija

def main():
    connection = connect_to_database()
    if connection:
        emails = fetch_emails_from_database(connection)
        if emails:
            svarigi_emails, jautajumi_emails, nenosakamie_emails = process_emails(emails)
            print_results(svarigi_emails, jautajumi_emails, nenosakamie_emails)
        connection.close()
    else:
        print("Pieslēgties datubāzei neizdevās.")


main()

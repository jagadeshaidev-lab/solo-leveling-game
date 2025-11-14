# --- test_notifier.py ---
# This file is ONLY for local testing. DO NOT PUSH TO GITHUB.

import os

# --- STEP A: PASTE YOUR REAL SECRETS HERE ---
# Ikkada nee 5 real secrets ni paste chey
os.environ['TWILIO_ACCOUNT_SID'] = "AC383e2107cac16a848fcd411b8e599f0c"
os.environ['TWILIO_AUTH_TOKEN'] = "4697aebd9d7b2cebe2181645f63f918b"
os.environ['TWILIO_FROM_NUMBER'] = "whatsapp:+14155238886"
os.environ['YOUR_WHATSAPP_NUMBER'] = "whatsapp:+919154625353"
os.environ['FIREBASE_CREDS_JSON'] = '{
  "type": "service_account",
  "project_id": "solo-leveling-tracker-65341",
  "private_key_id": "7e8f6a50e29b57c18022a6248fae3f4726ed521b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCRaM65A4auv1OI\nwiyzWLZ9E8W3MKQuj1fyZXIe40Bx4snzYYHgYc6RRgcoRubJeUPNCiSaHctR++HV\nWeb8nCOCJejwBlsJmpLEIhUOIyck5eKeT6kxVd+GLdmB2rmuUTXi45uJG5bMbg4J\nZaKxrx5JK6eTzP8SjdTTWEgTIz6LMCdekvVUWWdoFeqXObreH/fhQVmORQZcQALZ\ng42QARzlw1vQ3KUKDmZDeklm/vBrbKJkRpqItuRG/4o158/hTkRzhUnaQaLd5aPB\nuMieFagE/+PZcr2Va0PNFygLI4laf6PHyqfqABXcToG16tVC2+VRhb5nW+/D6DkR\n6ratQ0WfAgMBAAECgf9NE8FNUREs9nE3jOkk9Pr565rIzOY6lMEjPAlbvIC5dzD7\n62cGcAUoyULOyfm/BW8EwNumCSUKNpPL0MJTWApHP53tNwrXjGTZXzeWxthF0GJp\nVTcNb8RZQie8xxqlzDNEKy76Mb89neWfryaoCRHrHbjQH8BIyLKHu12sYOisqyaK\nCfCecXrhuAMiontX9KOoAPVWAC4LHCBLLsRP9XIRfSs5VcYSVgt+C2LBDEwH4Ebe\nJAtCLFR4J+Z4NSuUXhF8Nl3yNPEiaR9SwG052MdRagbfL5wOttYL8r0pk1LfLMT5\neWOx5sVw0XyK5WOeZ0GFMEYsNaZhTsUd58TiXVECgYEAy/1AKTroT3o+6kpSKaws\nbw4gVvIwWaamFM/1PbxzffzT5xSqkJrl2kPloCGA8HtxCj3QSZAFnvGHlLAJy9Lr\n8ViRAnxxlC7zWsbdJsiNEXoW8UZUo3BOi9o5m3JVu24P2ugpAJCvOPsu45DRlj2t\nun/lq90LxT5tq2m0FvfPLrECgYEAtnvxfhPQXU4+NHRuzEi1H4joYx/WM4MP5Pmx\nSWvva+xEFyPCBnYetLF/wx6Q9QkfzRQhNl95o/Tn4vyz3xrDlBc3t7E/Acb+oQQm\nnwvqTQjxWiu2YP71rgYjMFOKq7BCbjpKYEkb6mH9/IthcJuMurchTyukEsVSp0R2\nmnI67U8CgYBBVhE543tLEY2bP0jHvjTRMUYccyAXZvAlFGKpbnXTcapxhkYHYQWj\n/kFLI9AHtpIDRL81AKM8QII7lpLcrOcTe1me4TsDynH5rl5hMLU2VtOIXg13993A\nn5n59woMqXj8lYWkf7MP3iwriVQH+iNt688lV/yQJam80HN1M9QxUQKBgQCPCL10\nLkGvMQoPAYhrNT5K9nv4Xlb+T2eg+Zpdy22B8VI5tPx7JhDRXyOepBHJDxrPG00h\nGlr1CZzMzXiLkqXkKQKySArz8K9bNC61kZhYQ38yR3sPsiiN/B+O3JygEGsxjR0J\nNaTc5Ww4jGOW6UW4gJxqOvHDCMnNdBtm2cyYfwKBgFnmqeXZu+ucFoRfDhEdQelW\nbH/qv7gd8RE2mAHkSbz4mKWtygNtbVbuLM1xORpyPxO8pJDM+T2VBkV29IzX5Wqx\nKkCTh4Kx5mQ9xN3gew4snkWTanaZ6W1Y4AZDKOHQLzx8kFApe0RePhlcG2dYOx1p\nw0RS+pzPjxJvuBSUebE+\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@solo-leveling-tracker-65341.iam.gserviceaccount.com",
  "client_id": "116023978392851626726",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40solo-leveling-tracker-65341.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'

# --- STEP B: IMPORT THE REAL NOTIFIER SCRIPT ---
# Ippudu manam mana asalu script ni import chestunnam
from notifier import initialize_firebase_for_notifier, generate_and_send_eod_report

print("--- STARTING LOCAL TEST ---")

# --- STEP C: RUN THE TEST ---
print("Attempting to initialize Firebase...")
db = initialize_firebase_for_notifier()

if db:
    print("\nFirebase connection successful!")
    print("Attempting to generate and send EOD report to WhatsApp...")
    
    # Run the main function from our original script
    generate_and_send_eod_report(db)
    
    print("\nTest function execution finished.")
else:
    print("\nFirebase connection FAILED. Check your FIREBASE_CREDS_JSON.")

print("--- LOCAL TEST COMPLETE ---")

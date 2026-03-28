import re
import pyperclip

def normalize(text:str):
    text = text.replace("\n"," ")
    text=re.sub(r"\s+"," ", text)
    return text.strip()

def opd_data_valid(text: str):
    uhid=re.search(r"UHID\s*:\s*\S+", text, re.IGNORECASE)
    ipno=re.search(r"IP\s*NO\s*:\s*\d+",text,re.IGNORECASE)
    name=re.search(r"Patient\s*Name\s*:", text,re.IGNORECASE)
    age_gender=re.search(r"\d+\s*Years\s*/\s*(Male|Female)", text, re.IGNORECASE)
    opd_regno=re.search(r"Checkin\s*No\s*:\s*\S+", text,re.IGNORECASE)

    return bool(uhid and ipno and name and age_gender and opd_regno)

while True:
    input("Press enter after copying the patient data from HIS....")

    try:
        rawdata=pyperclip.paste()

        if not rawdata.strip():
            print("Clipboard is empty. Copy data first.")
            continue

        cleandata=normalize(rawdata).strip()

        if not opd_data_valid(cleandata):
            print("Invalid data on clipbard. Copy the valid data form HIS.\n")
            continue

        print("\n")
        print("Valid OPD data recieved.")
        print("."*30)
        print(f"{cleandata}")
        print("."*50)
        print("\n")

    except Exception as ex:
        print(f"Error occured: {ex}")
        continue

    choice=input("Fetch from another record (y/n): \n").strip().lower()
    if not choice.startswith("y"):
        break
    


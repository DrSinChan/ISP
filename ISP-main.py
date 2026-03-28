import re
import pyperclip
from rich import print
from rich.console import Console
console=Console()

#defining function to remove multiple lines, extra spaces between words and spaces in the begiinning and end of string
def normalize(text:str):
    text = text.replace("\n"," ")
    text=re.sub(r"\s+"," ", text)
    return text.strip()

#defining function to identify if the correct data is copied from HIS or not
def opd_data_valid(text:str):
    keyword1=re.search(r"UHID\s*:\s*\S+", text, flags=re.IGNORECASE)
    keyword2=re.search(r"IP\s*NO\s*:\s*\d+",text, flags=re.IGNORECASE)
    keyword3=re.search(r"Patient\s*Name\s*:", text, flags=re.IGNORECASE)
    keyword4=re.search(r"\d+\s*Years\s*/\s*(Male|Female)", text, flags=re.IGNORECASE)
    keyword5=re.search(r"Checkin\s*No\s*:\s*\S+", text, flags=re.IGNORECASE)
    return bool(keyword1 and keyword2 and keyword3 and keyword4 and keyword5)

#start of main program
while True:
    input("Press enter after copying the patient data from HIS....")

    try:
        rawdata=pyperclip.paste()

        if not rawdata.strip():
            print("Clipboard is empty. Copy data first.")
            continue
        
        #call function normalize() to clean spaces once it is identified clipboard is not empty.
        cleandata=normalize(rawdata).strip()

        #after removing spaces, call function opd_data_valid() to validate if the data copied is matching the required format in HIS or not
        if not opd_data_valid(cleandata):
            print("Invalid data on clipbard. Copy the valid data from HIS.\n")
            continue

        print("\n")   # returns empty line
        print("Valid OPD data recieved.")

        #print("."*30) #return 30 dots
        print(f"{cleandata}")
        #print("."*50) #return 50 dots

        print("\n") 

        #patient details format example
        #UHID : DL01.000012345 IP NO : 0123456789 Patient Name : Mr./Ms. Outdoor Age/Gender 34 Years / Male Checkin No : OPGESU022502720 Checkin Date
        #Time : 22-Feb-2025 05:54 AM Relationship : Self

        #parsing of relevant details of patient from above format
        ip_num=re.search(r"IP NO\s*:\s*(\d+)\s*patient name",cleandata, flags=re.IGNORECASE).group(1)
        pt_name=re.search(r"patient name\s*:\s*(.*?)\s*Age",cleandata, flags=re.IGNORECASE).group(1)
        
        pt_gender=re.search(r"\d+\s*year.\s*/\s*(.*?)\s*checkin no",cleandata, flags=re.IGNORECASE).group(1).title()
        checkin=re.search(r"checkin no\s*:\s*(.*?)\s*checkin datetime", cleandata, flags=re.IGNORECASE).group(1)

        #remove Mr/Ms related extra characters from the name
        clean_name=re.sub(r'^(Mr|Ms)\.?\s*/?\s*(Mr|Ms)?\.?\s*','',pt_name, flags=re.IGNORECASE).strip().title()
        
        try:
            pt_age=float(re.search(r".gender\s*(\d+)\s*year.",cleandata, flags=re.IGNORECASE).group(1))
            if not pt_age.is_integer():
                print("Invalid age or Error in fetching correct age.")
                continue
            else:
                age=int(pt_age)
        except ValueError:
            print("Invalid age or Error in fetching correct age.")
            continue


        if 1<=age<18:
            if pt_gender=="Male":
                pronoun="His"
                title="boy child"
            elif pt_gender=="Female":
                pronoun="Her"
                title="girl child"
            else:
                print("Invalid gender or Error in fetching correct gender.")
                continue
        elif age>=18:
            if pt_gender=="Male":
                pronoun="His"
                title="gentleman"
            elif pt_gender=="Female":
                pronoun="Her"
                title="lady"
            else:
                print("Invalid gender or Error in fetching correct gender.")
                continue
        else:
            print("Invalid age or Error in fetching correct age.")
            continue


        if age=="1":
            article="year"
        elif age>1:
            article="years"
        else:
            print("Invalid age or Error in fetching correct age.")
            continue

        console.print(
            "ESIC MEDICAL COLLEGE AND HOSPITAL",
            style="bold underline bright_red",
            justify="center"
            )
        
        console.print(
            f"A {age} {article} {pt_gender} {title} named as {clean_name} with IP No. - {ip_num}\nhas registered in OPD with OPD Checkin no. - {checkin}.",
            style="italic blue",
            justify="center"
            )
        console.print(
            " "*200,
            style="bold underline bright_red",
            justify="center"
            )
        
        print("."*10,"End of processing one record","."*10,"\n")

        
        
    except Exception as ex:
        print(f"Error occured: {ex}")
        continue

    choice=input("Fetch from another record (y/n): ").strip().lower()
    if not choice.startswith("y"):
        break
    


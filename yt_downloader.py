from msilib.schema import Directory
from os import link
from pytube import YouTube



link= input("Link: ")
directory = input("Directory: ")

try:
    yt = YouTube(link)
except:
    print("Invalid Link!")
    exit()


mp4s = yt.streams.filter(file_extension="mp4", progressive=True)

for i, mp4 in enumerate(mp4s):
    print(i+1, mp4)


n= int(input("Choose: "))

print("Downloading...")

mp4s[n-1].download(directory)

print("Download Completed!")




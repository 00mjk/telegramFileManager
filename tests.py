# THIS SCRIPT SHOULD BE EXECUTED ONLY BY THE MAKEFILE

# !!! dont run this on a channel that you have other files on, it will delete
# them !!!

from os import path
import pyrCaller
import sys
import config as cfg

data_path = "."
tmp_path = path.expanduser("~/.tmp")
telegram_channel_id = "me"
resumeTest = 0
toResume = True
progressUpload = []
progressDownload = []

if len(sys.argv) > 1:
    if sys.argv[1] == "resume1":
        resumeTest = 1
    elif sys.argv[1] == "resume2":
        resumeTest = 2

tmp_file = path.join(tmp_path, "tfilemgr", "rand")

def printProgress(current, total, current_chunk, total_chunks, sFile):
    global toResume
    prg=int(((current/total/total_chunks)+(current_chunk/total_chunks))*100)
    print("Progress of {}: {:3d}%".format(sFile, prg), end="\r", flush=True)
    if resumeTest and toResume and prg == 50:
        print("\nTest Resume")
        toResume = False
        tg.stop(resumeTest)


def fileDataFun(fileData=[], recvIndex=0, sFile=''):
    # recvIndex is only for uploading
    global progressDownload
    global progressUpload
    global index

    if fileData[1] == 1:
        progressUpload = fileData.copy()
        index = recvIndex
        print("{} {}".format(fileData, index))
    elif fileData[1] == 2:
        progressDownload = fileData.copy()
        print(fileData)

tg = pyrCaller.pyrogramFuncs(telegram_channel_id, cfg.api_id, cfg.api_hash,
                             data_path,tmp_path,"1",printProgress,fileDataFun)

print("Starting uploading of file")

# Do first time uploading and resuming upload in same function

inputFileData = [["temp/tfilemk_rand".split("/"), path.getsize(tmp_file), []],
                 tmp_file, 0]

fileData = tg.uploadFiles(inputFileData, 1)
if resumeTest:
    fileData = tg.uploadFiles(progressUpload, index)

toResume = True
print(fileData)
print("Starting downloading of file")
tg.downloadFiles([fileData[0], 0])
if resumeTest:
    tg.downloadFiles([progressDownload[0], progressDownload[2]])

print("Deleting temp files from telegram")
if input("this is very dangerous to run, make sure the telegram channel doesn't contain any other files, if you are sure type yes: ") == 'yes':
    tg.deleteUseless([0])
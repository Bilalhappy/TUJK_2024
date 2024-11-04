"""
GPS

"""
# ===========================================================
# ========================= imports =========================
import os
from ftplib import FTP_TLS
import subprocess
from pyunpack import Archive
import datetime
from dateutil.relativedelta import relativedelta
from gnsspy.funcs.funcs import (check_internet, obsFileName,
                                navFileName, nav3FileName, 
                                obs3FileName, datetime2doy)
# ===========================================================

__all__ = ["get_rinex", "get_rinex3", "get_navigation", "get_clock", "get_sp3", "get_ionosphere"]

email = "mutlubil@itu.edu.tr"
def download(ftp_dir,filename):
    ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
    ftps.login(user='anonymous', passwd=email)
    ftps.prot_p()
    ftps.cwd(ftp_dir[1:])
    ftps.retrbinary("RETR " + filename, open(filename, 'wb').write)
    
    
def get_rinex(stationList, date_start, date_finish=None, period='day', Datetime=False, directory=os.getcwd()):
    """
    This function downloads IGS rinex observation file from NASA CDDIS ftp server.
    
    Usage: 
        get_rinex(['mate'],'02-01-2017')
        get_rinex(['mate', 'onsa'],'01-01-2017')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '05-01-2017', period = 'day')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '01-06-2017', period = 'month')
        get_rinex(['mate', 'onsa'], date_start = '01-01-2017', date_finish = '03-01-2017', period = 'month')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '01-01-2018', period = 'year')
    """
    internet = check_internet()
    if internet == False:
        raise Warning('No internet connection! | Cannot download RINEX file...')
    
    if Datetime == False:
        date_start = datetime.date(year = int(date_start[-4:]), month = int(date_start[-7:-5]), day = int(date_start[-10:-8]))
        if date_finish != None:
            date_finish = datetime.date(year = int(date_finish[-4:]), month = int(date_finish[-7:-5]), day = int(date_finish[-10:-8]))
    
    timedelta = {'day'   : relativedelta(days   = 1),
                 'month' : relativedelta(months = 1),
                 'year'  : relativedelta(years  = 1)}[period]
    dateList = [date_start] # dates of observation files
    if date_finish != None:
        while dateList[-1] != date_finish:
            date = dateList[-1] + timedelta
            dateList.append(date)

    ftp_dir = '/pub/gps/data/daily' # observation file directory in ftp server
    
    for stationName in stationList:
        for date in dateList:
            doy = datetime2doy(date, string = True)
            fileName = obsFileName(stationName, date, zipped = True)
            fileName = fileName[:-3]+"m.gz"
            # check if the file already exist in the directory
            if os.path.exists(fileName)  == True:
                if os.path.exists(fileName[:-2])  == True:
                    print(fileName[:-2] + " exists in working directory")
                    continue
                else:
                    print(fileName + " exists in working directory | Extracting...")
                    #Archive(fileName).extractall(os.getcwd())
                    continue
            ftp_dir = '/pub/gps/data/daily'
            fileDir = [ftp_dir, str(date.year), doy, str(date.year)[-2:] + 'm/'] # file directory
            ftp_dir = '/'.join(fileDir)
            # Download the file
            try:
                print('Downloading:', fileName, end= '')
                print("\n Bura:  ",ftp_dir,fileName)
                download(ftp_dir,fileName)
                print(" | Download completed for", fileName, " | Extracting...")
                #Archive(fileName).extractall(os.getcwd())
            except:
                if os.path.exists(fileName)  == True:
                    os.remove(fileName)
                raise Warning("Requested file", fileName, "cannot be not found!")


def get_rinex3(stationList, date_start, date_finish=None, period='day', Datetime=False, directory=os.getcwd()):
    """
    This function downloads IGS rinex observation file from NASA CDDIS ftp server.
    
    Usage: 
        get_rinex(['mate'],'02-01-2017')
        get_rinex(['mate', 'onsa'],'01-01-2017')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '05-01-2017', period = 'day')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '01-06-2017', period = 'month')
        get_rinex(['mate', 'onsa'], date_start = '01-01-2017', date_finish = '03-01-2017', period = 'month')
        get_rinex(['mate'], date_start = '01-01-2017', date_finish = '01-01-2018', period = 'year')
    """
    internet = check_internet()
    if internet == False:
        raise Warning('No internet connection! | Cannot download RINEX file...')
    
    if Datetime == False:
        date_start = datetime.date(year = int(date_start[-4:]), month = int(date_start[-7:-5]), day = int(date_start[-10:-8]))
        if date_finish != None:
            date_finish = datetime.date(year = int(date_finish[-4:]), month = int(date_finish[-7:-5]), day = int(date_finish[-10:-8]))
    
    timedelta = {'day'   : relativedelta(days   = 1),
                 'month' : relativedelta(months = 1),
                 'year'  : relativedelta(years  = 1)}[period]
    dateList = [date_start]
    if date_finish != None:
        while dateList[-1] != date_finish:
            date = dateList[-1] + timedelta
            dateList.append(date)

    ftp_dir = '/pub/gps/data/daily' # observation file directory in ftp server
    
    for stationName in stationList:
        for date in dateList:
            doy = datetime2doy(date, string = True)
            fileName = obs3FileName(stationName, date, zipped = True)
            fileName = fileName[:-8]+"M.rnx.gz"
            # check if the file already exist in the directory
            if os.path.exists(fileName)  == True:
                if os.path.exists(fileName[:-2])  == True:
                    print(fileName[:-2] + " exists in working directory")
                    continue
                else:
                    print(fileName + " exists in working directory | Extracting...")
                    #Archive(fileName).extractall(os.getcwd())
                    continue
            fileDir = [ftp_dir, str(date.year), doy, str(date.year)[-2:] + 'm/']
            ftp_dir = '/'.join(fileDir) 
            try:
                print('Downloading:', fileName, end= '')
                download(ftp_dir,fileName) 
                print(" | Download completed for", fileName, " | Extracting...")
                #Archive(fileName).extractall(os.getcwd())
            except:
                if os.path.exists(fileName)  == True:
                    os.remove(fileName)
                raise Warning("Requested file", fileName, "cannot be not found!")


def runcmd(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

date1 = datetime.date(2021, 1, 1)

while True:
    while True:
        try:
            get_rinex3(['ista'],'{:02d}'.format(date1.day)+"-"+'{:02d}'.format(date1.month)+"-"+str(date1.year))
        except:
            try:
                get_rinex(['ista'], '{:02d}'.format(date1.day)+"-"+'{:02d}'.format(date1.month)+"-"+str(date1.year))
            except:
                break
        break
    date1 = date1 + datetime.timedelta(days=1)

    if date1.year==2022:
        break

runcmd("gunzip *.Z", verbose = True)

flist = [filename for filename in os.listdir(".") if filename.endswith("d") or filename.endswith("CRX")]

for f in flist:
    runcmd("./CRX2RNX "+f, verbose=True)
    runcmd("rm -rf "+f, verbose=True)

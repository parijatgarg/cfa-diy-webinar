import requests
import zipfile
import StringIO
import datetime
import dbutil


def download_nsecm_bhavcopy(bcdate):
    year = bcdate.year
    mnth = bcdate.strftime('%b').upper()
    dt = bcdate.strftime('%d')  
    base_path = "http://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}{}bhav.csv.zip"
    path =  base_path.format(year, mnth, dt, mnth, year)
    response = requests.get(path)
    if response.status_code == 200:
        response = response.content
    else:
        raise ValueError("Error downloading bhavcopy")
    nsezip = zipfile.ZipFile(StringIO.StringIO(response), 'r')
    filelist = nsezip.namelist()
    if len(filelist) > 1:
        raise ValueError("Something is wrong. More than one file found. Quitting.")
    for f in filelist:
        bhavcopyfile = nsezip.open(f, 'r')
        data = bhavcopyfile.read()
        compressed = dbutil.compress(data)
        filename = "marketsdata/nsecm.{}.bhavcopy.gz".format(
            bcdate.strftime('%Y%m%d'))
        with open(filename, 'w') as f:
            f.write(compressed)
    return True


def GetParser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('date')
    return parser


if __name__ == '__main__':
    args = GetParser().parse_args()
    date = datetime.datetime.strptime(args.date, '%Y%m%d')
    download_nsecm_bhavcopy(date)
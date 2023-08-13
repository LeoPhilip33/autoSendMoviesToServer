import os
import glob
import paramiko
from scp import SCPClient
from send2trash import send2trash
import config
from tqdm import tqdm

def sendFilm(movie):  
    nameMovie = os.path.basename(movie)
    localPath = os.path.join(config.localPath, nameMovie)
    remotePath = config.remotePath + '/' + nameMovie
    print(f"{nameMovie} movie Transfer")
    
    try:
        with ssh.open_sftp() as sftp:
            sftp.listdir(config.remotePath)
    except Exception as e:
        print(f"Error accessing remote folder: {e}")
    
    try:
        total_size = os.path.getsize(localPath)
        
        with tqdm(total=total_size, unit='B', unit_scale=True, miniters=1, desc=f"Transferring {nameMovie}") as pbar:
            def progress(filename, size, sent):
                pbar.update(sent - pbar.n)
            
            with SCPClient(ssh.get_transport(), progress=progress) as scp:
                scp.put(localPath, remotePath)
        
        print(f"Transfer completed for {nameMovie} movie.")
        
        send2trash(localPath)
        print(f"The movie {nameMovie} was trashed.")
    
    except Exception as e:
        print(f"Error transferring {nameMovie} movie. {e}")

movies = sorted(glob.glob(os.path.join(config.localPath, "*.mp4")))
lastElement = movies.pop()

print(f"{len(movies)} movies found.")
print("1. Send all available movies")
print("2. Exit")
choice = input("Enter your choice: ")

if choice == '1':
    if len(movies) >= 1:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            config.hostname,
            port=config.port,
            username=config.username,
            password=config.password,
            timeout=config.timeout
        )
        for movie in movies:
            sendFilm(movie)
        ssh.close()
    else:
        print('There are no films to send.')
    
elif choice == '2':
    print('Exiting...')
else:
    print('Invalid choice.')

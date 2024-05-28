from pytube import YouTube
from pytube import Playlist
from math import ceil
import sys
import threading
from tqdm import tqdm

try:
    p = Playlist(input("Enter Playlist URL: "))
except Exception as e:
    print(f"Error initializing playlist: {e}")
    sys.exit(0)

links = p.video_urls
size = ceil(len(links) / 4)

def split_link(links, size):
    for i in range(0, len(links), size):
        yield links[i:i + size]

link_chunks = list(split_link(links, size))

print("Downloading Started...\n")

def on_progress(progress_bar):
    def callback(stream, chunk, bytes_remaining):
        progress_bar.update(len(chunk))
    return callback

def downloader(link_chunk, thread_name):
    for i in link_chunk:
        try:
            yt = YouTube(i)
            ys = yt.streams.get_highest_resolution()
            
            with tqdm(total=ys.filesize, unit='B', unit_scale=True, desc=f"{thread_name} --> {yt.title[:30]}") as progress_bar:
                yt.register_on_progress_callback(on_progress(progress_bar))
                filename = ys.download()
            print(f"{thread_name} --> {filename.split('/')[-1]} Downloaded")
        except Exception as e:
            print(f"{thread_name} --> Failed to download {i}: {e}")

# Create and start threads
threads = []
for idx, link_chunk in enumerate(link_chunks):
    thread = threading.Thread(target=downloader, args=(link_chunk, f'threading {idx + 1}'))
    threads.append(thread)
    thread.start()

# Join threads to ensure completion
for thread in threads:
    thread.join()

print("All downloads completed.")
input("Press any key to exit...")  # Prompt for exiting the script

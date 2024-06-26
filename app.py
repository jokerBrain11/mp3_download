import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging
from datetime import datetime
from pytube import YouTube, Playlist, Search
from pydub import AudioSegment

class MP3Downloader:
    def __init__(self, master):
        self.master = master
        self.master.title("MP3 Downloader")

        current_directory = os.getcwd()
        self.default_dir = os.path.expanduser(f"{current_directory}/downloads") # 預設下載目錄(/downloads)

        self.url_label = tk.Label(master, text="URL or Keyword:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.bitrate_label = tk.Label(master, text="Bitrate (kbps):")
        self.bitrate_label.pack()

        self.bitrate_entry = tk.Entry(master, width=10)
        self.bitrate_entry.insert(0, "128")
        self.bitrate_entry.pack()

        self.download_button = tk.Button(master, text="Download", command=self.download_mp3)
        self.download_button.pack()

        self.save_dir = self.default_dir
        self.choose_dir_button = tk.Button(master, text="Choose Download Directory", command=self.choose_directory)
        self.choose_dir_button.pack()

        self.setup_logging()

    def setup_logging(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
        log_filepath = os.path.join(log_dir, log_filename)
        logging.basicConfig(filename=log_filepath, level=logging.INFO, format='%(asctime)s - %(message)s')

    def log_message(self, message):
        logging.info(message)

    def choose_directory(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.save_dir = selected_dir
            messagebox.showinfo("Directory Selected", f"Files will be saved to: {self.save_dir}")
        else:
            messagebox.showinfo("Directory Not Selected", f"No directory selected. Using default directory: {self.save_dir}")

    def download_mp3(self):
        url_or_keyword = self.url_entry.get()
        bitrate = self.bitrate_entry.get()
        if not bitrate.isdigit() or int(bitrate) <= 0:
            messagebox.showerror("Error", "Please enter a valid bitrate.")
            self.log_message(f"Invalid bitrate: {bitrate}")
            return

        self.log_message(f"Starting download for: {url_or_keyword} with bitrate: {bitrate}")
        if url_or_keyword.startswith("http"):
            if "list" in url_or_keyword:
                self.download_playlist(url_or_keyword, bitrate)
            else:
                self.download_from_url(url_or_keyword, bitrate)
        else:
            self.search_and_download(url_or_keyword, bitrate)

    def download_from_url(self, url, bitrate):
        try:
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            output_file = audio_stream.download(output_path=self.save_dir)
            base, ext = os.path.splitext(output_file)
            new_file = base + '.mp3'
            self.convert_to_mp3(output_file, new_file, bitrate)
            os.remove(output_file)  # 删除原始文件
            self.log_message(f"Download complete for: {url}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_message(f"Error downloading {url}: {str(e)}")

    def download_playlist(self, url, bitrate):
        try:
            playlist = Playlist(url)
            for video_url in playlist.video_urls:
                self.download_from_url(video_url, bitrate)
            messagebox.showinfo("Success", "Playlist download complete!")
            self.log_message(f"Playlist download complete for: {url}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log_message(f"Error downloading playlist {url}: {str(e)}")

    def search_and_download(self, keyword, bitrate):
        try:
            search = Search(keyword)
            video = search.results[0]
            self.download_from_url(video.watch_url, bitrate)
        except Exception as e:
            messagebox.showerror("Error", "No videos found for the given keyword or unable to download.")
            self.log_message(f"No videos found or unable to download for keyword: {keyword}")

    def convert_to_mp3(self, input_file, output_file, bitrate):
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="mp3", bitrate=f"{bitrate}k")

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Downloader(root)
    root.mainloop()

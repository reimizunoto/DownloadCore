# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys
import subprocess
import os

count = 1
class DownloadcorePipeline:
    def process_item(self, item, spider):
        if spider.name == "rrys":
            # process rrys item
            self._rrys(item)
        if spider.name == "bilibili":
            self._bilibili(item)
        if spider.name == "iyhdmm":
            self._iyhdmm(item)
        if spider.name == "netease_music":
            self._netease_music(item)
        if spider.name == "huohutv":
            self._huohutv(item)
        if spider.name == "tvyb10":
            self._tvyb10(item)
            
    def _rrys(self, item):
        global count
        with open(f"video/{item['title']}.mp4", "ab+") as f:
            f.write(item["video_ts"])
            print(f"正在保存第{count}个ts文件：")
            count += 1
        print("视频下载完成，大小为：", sys.getsizeof(item["video_ts"])/1024/1024, "MB")
        
    def _bilibili(self, item):
        if item["video"] is None or item["audio"] is None:
            return
        video_path = 'video/video.m4s'
        audio_path = 'video/audio.m4s'
        mp4_path = f'video/{item["title"]}.mp4'
        print("开始下载视频和音频...")
        # 保存临时视频和音频
        try:
            with open(video_path, "wb") as f:
                f.write(item["video"])
                print("视频保存成功，大小为：", sys.getsizeof(item["video"])/1024/1024, "MB")
        except Exception as e:
            print("视频保存失败：", e)
        try:
            with open(audio_path, "wb") as f:
                f.write(item["audio"])
                print("音频保存成功，大小为：", sys.getsizeof(item["audio"])/1024/1024, "MB")
        except Exception as e:
            print("音频保存失败：", e)
            
        # 合并视频和音频
        print("开始合并视频和音频...")
        ffmpeg_cmd = f"ffmpeg -i {video_path} -i {audio_path} -c copy \"{mp4_path}\""
        subprocess.call(ffmpeg_cmd, shell=True)
        # 删除临时文件
        os.remove(video_path)
        os.remove(audio_path)
        print("视频合并完成，大小为：", os.path.getsize(mp4_path)/1024/1024, "MB")
    
    def _iyhdmm(self, item):
        global count
        count = 1
        with open(f"video/{item['title']}.mp4", "ab+") as f:
            f.write(item["video"])
            print(f"正在保存第{count}个ts文件：")
            count += 1
        print("视频下载完成，大小为：", sys.getsizeof(item["video_ts"])/1024/1024, "MB")
        
    def _netease_music(self, item):
        music_path = f'music/{item['music_name']}.m4a'
        print(f"开始保存音乐{item['music_name']}...")
        with open(music_path, "wb") as f:
            f.write(item["music"])
            print(f"音乐{item['music_name']}保存完成，大小为：", sys.getsizeof(item["music"])/1024/1024, "MB")
        
    def _huohutv(self, item):
        global count
        video_path = f'video/{item["title"]}.mp4'
        print(f"开始保存视频{item['title']}...")
        with open(video_path, "ab+") as f:
            f.write(item["video"])
            print(f'正在保存第{count}个ts文件')
            count += 1
            
    def _tvyb10(self, item):
        global count
        video_path = f'video/{item["title"]}.mp4'
        print(f"开始保存视频{item['title']}...")
        with open(video_path, "ab+") as f:
            f.write(item["video"])
            print(f'正在保存第{count}个ts文件')
            count += 1
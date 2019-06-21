"""
file: preparator.py
author: Mikhail Visloguzov m.visloguzov@ya.ru

Файл предназначен для разбиения видеофайлов на мальенькие кусочки для создания из них карточек Anki.
Из видеофалов вытаскивается аудиодорожки, кусочки видео преобразуюстся в gif etc.
"""

import subprocess
import glob
import os
#subprocess.run(["ls", "-l"])
#subprocess.run("ls")

files_path = "/Users/mivi/heap/avatar/parts/"
#files = glob.glob("/Users/mivi/heap/avatar/parts/*.mkv")

files = [f for f in glob.glob(files_path + "**/*.mkv", recursive=True)]

os.chdir(files_path)
for f in files:
    print(f)
    file_name_without_extension = os.path.splitext(f)[0]
    #Превращаем в gif:
    command = "ffmpeg -i {} -filter_complex \"[0:v] fps=12,scale=480:-1,split [a][b];[a] palettegen=max_colors=56 [p];[b][p] paletteuse=dither=bayer:bayer_scale=1:diff_mode=rectangle\" {}.gif"
    #subprocess.run(command.format(f))
    subprocess.call( command.format(f, file_name_without_extension), shell=True )



"""
brew install mkvtoolnix - установить в мак

Удалил русскую дорожку, оставив английскую и оба варианта субтитров
mkvmerge -o S01E03.mkv --atracks 0,2,3,4 Avatar.The.Last.Airbender.S01E03.The.Southern.Air.Temple.1080p.mkv

mkvmerge -o out.mkv --split 1s output.mkv 
Похоже split по времени лучше выдает чем split по размеру

Превращаем в gif:
ffmpeg -i out-314.mkv -filter_complex "[0:v] fps=12,scale=480:-1,split [a][b];[a] palettegen=max_colors=56 [p];[b][p] paletteuse=dither=bayer:bayer_scale=1:diff_mode=rectangle" 314.gif


Вшить субтитры в видео
ffmpeg -i out-320.mkv -vf subtitles=out-320.mkv out-320s.mkv  НАВЕРОЕ ЭТО МОЖНО СДЕЛАТЬ ОДНОЙ КОМАНДОЙ С РАЗБИЕНИЕМ НА КУСОЧКИ ???
https://video.stackexchange.com/questions/15395/how-to-split-a-large-mkv-file-into-parts-with-the-srt-subtitle-file-separated

https://blog.programster.org/strip-audio-tracks-from-an-mkv-with-mkvtoolnix

https://www.easytechguides.com/remove-hardcoded-subtitles-from-mkv-video-files.html

https://superuser.com/questions/98399/remove-embedded-subtitles-from-an-mkv-file

https://video.stackexchange.com/questions/15395/how-to-split-a-large-mkv-file-into-parts-with-the-srt-subtitle-file-separated

План как буду делать:
1 убрать русскую дорожку
2 разбить на кусочки в отдельный каталог 
Вшить в видео английские субтитры, чтобы видеть их поверх gif ??
3 каждый кусочек превратить в name.gif
4 из каждого кусочка вытащить русские субтитры в файл name.txt
5  из каждого кусочка вытащить English subs и добавить в тот же файл name.txt
6 из каждого кусочка вытащить аудиодорожку

"""
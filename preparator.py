"""
file: preparator.py
author: Mikhail Visloguzov m.visloguzov@ya.ru

Файл предназначен для разбиения видеофайлов на маленькие кусочки для создания из них карточек Anki.
Из видеофалов вытаскивается аудиодорожки, кусочки видео преобразуюстся в gif etc.
"""
import subprocess
import os

#mkvextract tracks out-320.mkv 4:320rusub.txt
#subprocess.call(["ls", "-l", "."])

out_dir_name = "out"
video_pieces_dir = "pieces"
pieces_pattern = "{0}/{1}/{2}.mkv"
pieces_dir = "/{0}/{1}/".format(out_dir_name, video_pieces_dir)
source_file = "S01E06.mkv";
source_file_name = source_file.replace('.mkv','')
name_begin = source_file_name

path = os.getcwd() + pieces_dir

try:
    os.makedirs(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

# Режем исходный файл на кусочки и кладем в каталог.
# mkvmerge -o out/o.mkv --split 1s SO1E06.mkv
piece = pieces_pattern.format(out_dir_name, video_pieces_dir, name_begin)
subprocess.call(["mkvmerge", "-o", piece, "--split", "1s", source_file])

def extract_from_piece( piece_name, out_dir_name, video_pieces_dir, work_file ):
    #part_file_name = "Python is as simple as {0}, {1}, {2}".format("a", "b", "c")
    # Кусок фильма, из которого будем вытаскивать треки
    
    rusub_dir_name = "rusub"
    engsub_dir_name = "engsub"
    audio_dir_name = "audio"
    gif_dir = "gifs"
    
    
    
    mkvextract = "mkvextract"
    tracks = "tracks"
    rusub_file = "2:{0}/{1}/{2}.txt"
    engsub_file = "3:{0}/{1}/{2}.txt"
    audio_file = "{0}/{1}.mp3"
    gif_file = "{0}/{1}/{2}.gif"
    
    path = os.getcwd() + "/{0}/{1}"
    
    try:
        os.makedirs(path.format(out_dir_name, gif_dir))
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    
    # Вытаскиваю русские субтитры
    subprocess.call([mkvextract, tracks , work_file, rusub_file.format(out_dir_name, rusub_dir_name, piece_name)])

# Вытаскиваю английские субтитры
subprocess.call([mkvextract, tracks, work_file, engsub_file.format(out_dir_name, engsub_dir_name, piece_name)])
    
    # Вытаскиваю аудио дорожку
    # subprocess.call([mkvextract, tracks, work_file, audio_file.format(out_dir_name, audio_dir_name, piece_name)]) - при таком способе mp3 несовсем корректный, не
    # овспроизводится на мобильной версии анки
    # ffmpeg -i out-320s.mkv -vn -ar 44100 -ac 2 -ab 192K -f mp3 sound.mp3
    # subprocess.call(['ffmpeg', '-i', work_file, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192K', '-f', 'mp3', audio_file.format(out_dir_name, audio_dir_name, piece_name)])
    subprocess.call(["ffmpeg", "-i", work_file, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192K", "-f", "mp3", audio_file.format(out_dir_name, piece_name)])
    
    
    #делаю gif из этого кусочка
    #ffmpeg -i out-320s.mkv -filter_complex "[0:v] fps=12,scale=480:-1,split [a][b];[a] palettegen=max_colors=56 [p];[b][p] paletteuse=dither=bayer:bayer_scale=1:diff_mode=rectangle" 320.gif
    command = "[0:v] fps=12,scale=480:-1,split [a][b];[a] palettegen=max_colors=56 [p];[b][p] paletteuse=dither=bayer:bayer_scale=1:diff_mode=rectangle"
    subprocess.call(["ffmpeg", "-i" , work_file, "-filter_complex", command, gif_file.format(out_dir_name, gif_dir, piece_name)])
    return

#extract_from_piece( piece_name, out_dir_name, video_pieces_dir )

directory = os.getcwd() + pieces_dir

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".mkv") :
        base = os.path.basename(filename)
        #print(os.path.join(directory, filename))
        base = os.path.splitext(base)[0]
        #piece_name = base.replace(name_begin + '-','')
        part_file_name = "{0}/{1}/{2}.mkv"
        work_file = part_file_name.format(out_dir_name, video_pieces_dir, base)
        extract_from_piece( base, out_dir_name, video_pieces_dir, work_file )
        continue
    else:
        continue

for %%f in (*.mp4) do ffmpeg -i "%%f" -ss 00:00:01 -vframes 1 -s 256x144 "%%~nf".png
for %%f in (*.webm) do ffmpeg -i "%%f" -ss 00:00:01 -vframes 1 -s 256x144 "%%~nf".png
pause

### Example Command
```bash
ffmpeg -f concat -safe 0 -i run.txt -i "tests\imgs\a.m4a" -vf "scale=1280:720,format=yuv420p" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 192k -shortes
t output.mp4
```
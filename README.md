# pi_streaming
Stream live camera on Raspberry Pi using HLS, MPEG-DASH, MJPEG (MJPG), and H264.

## HLS/ DASH
This streaming method can stream H264 video chunks with some advantages from adaptive bitrate but it has delay of more than 3 seconds.

Read more at: https://www.codeinsideout.com/blog/pi/stream_ffmpeg_hls_dash/

## MPJEG
This can archive low-latency streaming for video but it consumes a lot of network bandwidth due to the size of each JPEG frame

Read more at: https://www.codeinsideout.com/blog/pi/stream_picamera_mjpeg/

## H264
This method streams H264 NAL units to clients so that it can keep low bandwidth and low latency.

Read more at: https://www.codeinsideout.com/blog/pi/stream_picamera_h264/

Find more about Raspberry Pi and embedded system at [Code Inside Out](https://www.codeinsideout.com/)

# License

MIT License

# 帧区间与导出检查

每行描述一段已确定的配音。`seconds` 是实测音频秒数，`pause_after` 是额外进入时间线的静音。音频里已经包含的停顿不要重复计入。`fps` 是目标整数帧率，`id` 必须唯一。

```json
{"fps":30,"segments":[{"id":"intro","seconds":1.25,"pause_after":0.15},{"id":"demo","seconds":2.1}]}
```

```bash
python3 scripts/plan_frames.py timing.json
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,avg_frame_rate:format=duration -of json clip.mp4
```

脚本对累计时间取最近帧，并给出半开区间 `[start_frame, end_frame)`。`speech_end_frame` 是语音结束点；段后停顿占据本段最后的部分。上例首段到第 42 帧结束，下一段从第 42 帧开始，全片 105 帧。读取音频和视频文件时，以 FFprobe 流信息核实实际输出。

检查每一种交付画幅的第一帧、最长标题、转场和尾帧。字幕避开视频中已有的核心文字；不同时刻的字幕有实际变化。逐帧查看时无法判断音量和口播自然度，需要另作试听。

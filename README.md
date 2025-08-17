## Requirements

- **Python 3.12** (install from Windows Store)
- Optional: **FFmpeg** (for audio trimming)

## Usage

```bash
python vv2.py
```

## Non-Korean Configuration

Please modify the following parts of the `config.json`:

```
"LANG": 'en',
"PROMPT": 
"Listen to the dermatology consultation recording and summarize it in 1-4 short lines for charting purposes. Use very brief, single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. :",
"PROMPT2": 
"Listen to the dermatology consultation recording and create a medical chart. Try to keep sentences brief and in single-answer style. For example: '3MA mild itch on back', 'widespread rash of unknown duration', 'r/o shingles', 'medication from another hospital', 'return in 3 days'. If the patient presents with multiple issues, separate them by issue and only record facts mentioned in the conversation. :"
```

![Screenshot](screenshot.png)

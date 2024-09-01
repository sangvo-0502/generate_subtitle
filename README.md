# Generate Subtitles for Videos using Whisper from OpenAI (100% local on MacOS)

## Introduction

Subtitles play a crucial role in making videos accessible to a global audience. Whether you're sharing a tutorial, a lecture, or entertainment content, providing subtitles in multiple languages can significantly enhance your video's reach. But manually creating subtitles in different languages is a time-consuming task.
For me, I used it for generating subtitles for my favourite films.

This is where **Whisper by OpenAI** comes in—a powerful tool that leverages cutting-edge AI to generate accurate subtitles in various languages, helping you automate and streamline this process.

![image](https://github.com/user-attachments/assets/fed05a0e-3070-4a33-9822-2b2899697dd9)


## What is Whisper?

[Whisper](https://github.com/openai/whisper) is an open-source automatic speech recognition (ASR) system developed by OpenAI. It is designed to transcribe speech to text with high accuracy, supporting a wide range of languages. It can also translate subtitles directly into different languages, making it an incredibly versatile tool for content creators.

## Key Features

- **Multi-language Support:** Whisper supports over 50 languages, making it a go-to solution for global content. (you can change the language code: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes)
- **High Accuracy:** Whisper is trained on a large dataset, resulting in high transcription accuracy.
- **Ease of Use:** With a simple command-line interface, you can generate subtitles with just a few commands.
- **Translation Capabilities:** Whisper can not only transcribe but also translate the transcription into multiple languages.

  **Note: this is for MacOS, you can still use it on Window but should follow the instruction for Window installation (https://github.com/openai/whisper). 

## How to Use Whisper to Generate Subtitles


### Installation

First, you'll need to install Whisper. You can do this using pip:

```bash
pip install git+https://github.com/openai/whisper.git
```

Secondly, create 4 folders like this (you can rename them):

    ```
    videos_folder = "/Users/administrator/Documents/test/video/"
    output_folder = "/Users/administrator/Documents/test/audio/"
    json_output_folder = "/Users/administrator/Documents/test/json/"
    srt_output_folder =  "/Users/administrator/Documents/test/srt/"
    ```
Thirdly, open terminal and run (this will help to avoid out of memory)

```bash
export pytorch_enable_mps_fallback=1
```
Finally, run (in terminal) 

```bash
python transcribe_chinese.py ##change your language and filename
```







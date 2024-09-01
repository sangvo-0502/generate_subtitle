# Generate Subtitles for Videos using Whisper from OpenAI (100% local on MacOS)

## Introduction

Subtitles play a crucial role in making videos accessible to a global audience. Whether you're sharing a tutorial, a lecture, or entertainment content, providing subtitles in multiple languages can significantly enhance your video's reach. But manually creating subtitles in different languages is a time-consuming task.
For me, I used it for generating subtitles for my favourite films.

This is where **Whisper by OpenAI** comes in—a powerful tool that leverages cutting-edge AI to generate accurate subtitles in various languages, helping you automate and streamline this process.

![image](https://github.com/user-attachments/assets/fed05a0e-3070-4a33-9822-2b2899697dd9)


## What is Whisper?

[Whisper](https://github.com/openai/whisper) is an open-source automatic speech recognition (ASR) system developed by OpenAI. It is designed to transcribe speech to text with high accuracy, supporting a wide range of languages. It can also translate subtitles directly into different languages, making it an incredibly versatile tool for content creators.

## Key Features

- **Multi-language Support:** Whisper supports over 50 languages, making it a go-to solution for global content.
- **High Accuracy:** Whisper is trained on a large dataset, resulting in high transcription accuracy.
- **Ease of Use:** With a simple command-line interface, you can generate subtitles with just a few commands.
- **Translation Capabilities:** Whisper can not only transcribe but also translate the transcription into multiple languages.

  **Note: this is for MacOS, you can still use it on Window but should follow the instruction for [Window installation]([url](https://github.com/openai/whisper)). 

## How to Use Whisper to Generate Subtitles


### 1. Installation

First, you'll need to install Whisper. You can do this using pip:

```bash
pip install git+https://github.com/openai/whisper.git

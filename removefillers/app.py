from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS  # Import the CORS module
from moviepy.editor import VideoFileClip
import whisper_timestamped as whisper
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['TMP'] = 'tmp'
app.config['AUDIO'] = 'audio'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

if not os.path.exists(app.config['TMP']):
    os.makedirs(app.config['TMP'])

if not os.path.exists(app.config['AUDIO']):
    os.makedirs(app.config['AUDIO'])    

def extract_audio_from_video(video_path, filename):
    # Step 1: Extract audio from video
    # video_path = "/Users/kamal/Movies/chatgpt_footage/codep3.mkv"
    video = VideoFileClip(video_path)
    audio_file_path = os.path.join(app.config['AUDIO'], filename.split('.')[0] + '.wav')
    video.audio.write_audiofile(audio_file_path)
    return audio_file_path

def whisper_transcribe(audio_file_path):

    audio = whisper.load_audio(audio_file_path)

    model = whisper.load_model("tiny", device="cpu")

    result = whisper.transcribe(model, audio, detect_disfluencies=True, language="en")

    return result

def process_filler_words(result):
    filler_words=[]

    for text in result["segments"]:
        for word in text["words"]:
            if "[*]" in word["text"]:
                filler_words.append([word["start"], word["end"]])
                final_end_time = result["segments"][-1]["end"]


    split_times = []
    for i in range(len(filler_words)):
        if i == 0:
            start = 0
            end = filler_words[i][0]
        else:
            start = filler_words[i-1][1]
            end = filler_words[i][0]  
            filler_words[i]
            
        split_times.append([start, end])
    
    split_times.append([filler_words[-1][1], final_end_time])
    return split_times

def generate_and_join_subclips(uploaded_file_path, output_filename, split_times):
    ### split
    for i in range(len(split_times)):
        start_time = split_times[i][0]
        end_time = split_times[i][1]
        ffmpeg_extract_subclip(uploaded_file_path, start_time, end_time, targetname=f"{app.config['TMP']}/"+str(i)+".mp4")
    ### concatenate
    clips=[]
    for i in range(len(split_times)):
        clip = f"{app.config['TMP']}/"+str(i)+".mp4"
        clips = clips + [VideoFileClip(clip)]

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(f"{app.config['OUTPUT_FOLDER']}"+"/"+f"{output_filename.split('.')[-2]}"+".mp4")
    
    ## delete all files in tmp folder
    for i in range(len(split_times)):
        os.remove(f"{app.config['TMP']}/"+str(i)+".mp4")


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']

        # Save the uploaded file
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(uploaded_file_path)

        # Process the uploaded video here (modify video)
        # For this example, we'll just copy the uploaded video to the output folder
        audio_file_path = extract_audio_from_video(uploaded_file_path, uploaded_file.filename)
        result = whisper_transcribe(audio_file_path)
        split_times = process_filler_words(result)
        generate_and_join_subclips(uploaded_file_path, uploaded_file.filename, split_times)

        # Provide the download URL for the processed video
        download_url = f'http://127.0.0.1:5000/download/{uploaded_file.filename.split(".")[-2]}'+'.mp4'

        response = {'message': 'File uploaded and processed successfully.', 'download_url': download_url}
        return jsonify(response), 200
    except Exception as e:
        response = {'message': 'An error occurred: ' + str(e)}
        return jsonify(response), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

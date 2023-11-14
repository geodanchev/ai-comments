from io import StringIO
from anyio import Path
import webvtt
from webvtt.errors import MalformedCaptionError
from tempfile import NamedTemporaryFile

# extracts all meaningful content

def read_vtt_file(file):
    captions = []

    for caption in webvtt.read(file):
        captions.append(caption.text.replace('\n', ' '))

    return captions


def read_vtt_file_from_request_content(decodedContent, extension):
    result = []
    with NamedTemporaryFile('w', suffix=f'.{extension}', delete=False) as temp_file:
        temp_file.write(decodedContent)
        temp_file.close()
        result = read_vtt_file(temp_file.name)
    return result


if __name__ == '__main__':

    vtt_file_path = '.\\static\\uploads\\dummy.vtt'

    if Path(vtt_file_path).exists():
        meaningful_text = read_vtt_file(vtt_file_path)
        print(meaningful_text)
    else:
        print(f"Could not find the VTT file at path: {vtt_file_path}")

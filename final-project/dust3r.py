import requests
import os

def send_request(glb_file_path):
    print("Sending request to HuggingFace endpoint")
    url = "https://tur-learning-dust3r-fastapi.hf.space/upload_zip/"
    output_file_path = "./model.glb"

    # Load the file
    files = {'file': open(glb_file_path, 'rb')}

    # Send the POST request
    response = requests.post(url, files=files)

    # Save the response to the output file
    if response.status_code == 200:
        with open(output_file_path, 'wb') as f:
            f.write(response.content)
        print("File saved!")
    else:
        print(f"Error during file loading: {response.status_code}")


if __name__ == "__main__":
    send_request("photos.zip")
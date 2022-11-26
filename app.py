from fastapi import FastAPI, File, UploadFile
import uvicorn
import os
import time

cwd = os.getcwd()

def remove_old_files(directory='inputs'):
    ago  = time.time() - (1)
    root = cwd + "/" + directory

    for i in os.listdir(root):
        path = os.path.join(root, i)
        old = os.stat(path).st_mtime <= ago
        png = os.path.splitext(path)[1] == ".png"
        if os.path.isfile(path) and old and png:
            os.remove(path)

app = FastAPI()

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    remove_old_files('inputs')
    remove_old_files('outputs')
    # todo allow only png files
    try:
        contents = file.file.read()
        with open('inputs/' + file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    os.system("python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs -o outputs --outscale 2")

    return {"message": f"Successfully uploaded {file.filename}"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
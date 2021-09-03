import os
from models import Noise2Same
import gradio as gr

# load the model
os.system("mkdir trained_models/denoising_ImageNet")
os.system("cd trained_models/denoising_ImageNet; gdown https://drive.google.com/uc?id=1asrwULW1lDFasystBc3UfShh5EeTHpkW; gdown https://drive.google.com/uc?id=1Re1ER7KtujBunN0-74QmYrrOx77WpVXK; gdown https://drive.google.com/uc?id=1QdlyUPUKyyGtqD0zBrj5F7qQZtmUELSu; gdown https://drive.google.com/uc?id=1LQsYR26ldHebcdQtP2zt4Mh-ZH9vXQ2S; gdown https://drive.google.com/uc?id=1AxTDD4dS0DtzmBywjGyeJYgDrw-XjYbc; gdown https://drive.google.com/uc?id=1w4UdNAbOjvWSL0Jgbq8_hCniaxqsbLaQ; cd ../..")
model = Noise2Same('trained_models/', 'denoising_ImageNet', dim=2, in_channels=3)
    
# define the prediction function
def predict(img):
  pred = model.predict(img.astype('float32'))
  pred = (pred-pred.min())/(pred.max()-pred.min())
  return pred

# launch a gradio interface
gr.Interface(predict, "image", "image").launch()
from Blind_Watermark import encode, decode
from DWT_DCT_Image_Watermarking import DWT_DCT_technique
from DWT_SVD import DWT_SVD_technique
from Robust_Watermarking import embedDCT, extract
from DCT_DWT_SVD_watermarking_technique import embed
from DCT_DWT_SVD_watermarking_technique import functions as f
import functionsAlgorithms
import glob


#Quale watermark verrà utilizzato
watermark="./Watermark/watermark.png"

#Quali immagini verrano prese in input dagli algoritmi di watermarking
def switch(val, watermark):
    image_path=glob.glob("./Images/"+"*.jpeg", recursive=True)


    if val == "DFT-BlindWatermark":
        for path in image_path:
            print("Encoding...")
            res=encode.main(path, watermark)
            print("Decoding...")
            decode.main(path, res)
    if val == "DWT-DCT Watermarking":
        for path in image_path:
            DWT_DCT_technique.w2d(path, watermark)
    if val == "DWT-SVD Watermarking":
        for path in image_path:
           DWT_SVD_technique.launch(path, watermark)
    if val == "DCT Watermarking":
        for path in image_path:
            res=embedDCT.main(path, watermark)
            extract.main(res)
    if val == "DWTonly":
        for path in image_path:
            functionsAlgorithms.DWT(path, watermark)
    if val == "DCTonly":
        for path in image_path:
            functionsAlgorithms.DCT(path, watermark)
    if val == "DFTonly":
        for path in image_path:
            functionsAlgorithms.DFT(path, watermark)
    if val == "SVDonly":
        for path in image_path:
            functionsAlgorithms.SVD(path, watermark)
    if val == "DWT_SVD":
        for path in image_path:
            functionsAlgorithms.DWT_SVD(path, watermark)
    if val == "DWT_DCT_SVD":
        for path in image_path:
            functionsAlgorithms.DWT_DCT_SVD(path, watermark)
    if val == "DCT_DWT_SVD_npy":
        embedDCT.main()






options = {"1": "DFT-BlindWatermark",
           "2": "DWT-DCT Watermarking",
           "3": "DWT-SVD Watermarking",
           "4": "DCT Watermarking",
           "5": "DWTonly",
           "6": "DCTonly",
           "7": "DFTonly",
           "8": "SVDonly",
           "9": "DWT_SVD",
           "10": "DWT_DCT_SVD",
           "11": "DCT_DWT_SVD_npy"

               }
val = input('What type of embedding you want to perform?\n1.DFT-BlindWatermark\n2.DWT-DCT Watermarking\n3.DWT-SVD Watermarking\n4.DCT Watermarking\n5.DWTonly\n6.DCTonly\n7.DFTonly\n8.SVDonly\n9.DWT_SVD\n10.DWT_DCT_SVD\n11.DCT_DWT_SVD_npy')
print("Running " + options[val])

switch(options[val], watermark)





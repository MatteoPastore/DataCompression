from Blind_Watermark import encode, decode
from DWT_DCT_Image_Watermarking import DWT_DCT_technique
from DWT_SVD import DWT_SVD_technique
from Robust_Watermarking import embedDCT, extract
from DCT_DWT_SVD_watermarking_technique import embed, ber, check_diffs, test_attacks


from DCT_DWT_SVD_watermarking_technique import functions as f
import functionsAlgorithms
import glob
import watermarkNpy512



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
    if val == "Exit":
        print("No embedding selected")






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
           "11": "DCT_DWT_SVD_npy",
           "12": "Exit"

               }
val = input('What type of embedding you want to perform?\n1.DFT-BlindWatermark\n2.DWT-DCT Watermarking\n3.DWT-SVD Watermarking\n4.DCT Watermarking\n5.DWTonly\n6.DCTonly\n7.DFTonly\n8.SVDonly\n9.DWT_SVD\n10.DWT_DCT_SVD\n11.DCT_DWT_SVD_npy\n12.Exit')
print("Running " + options[val])

switch(options[val], watermark)

print("DONE")




def switchTesting(val):
    image_path=glob.glob("./imagesToAttack/"+"*.*", recursive=True)
    if val == "Bit Error Ratio":
        for path in image_path:
            ber.main(path)
    if val == "Check Differences between images":
        check_diffs.main()
    if val == "Test Attacks on image":
        test_attacks.main()
    if val == "Exit":
        print("No testing selected")





optionsTesting = {"1": "Bit Error Ratio",
           "2": "Check Differences between images",
           "3": "Test Attacks on image",
           "4": "Exit"


               }
valTesting = input('What type of testing you want to perform?\n1.Bit Error Ratio\n2.Check Differences between images\n3.Test Attacks on image\n4.Exit')
print("Running " + optionsTesting[valTesting])
switchTesting(optionsTesting[valTesting])


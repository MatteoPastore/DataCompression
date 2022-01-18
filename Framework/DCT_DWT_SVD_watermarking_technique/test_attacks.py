from DCT_DWT_SVD_watermarking_technique import attacks
from DCT_DWT_SVD_watermarking_technique import embed
import numpy as np
from DCT_DWT_SVD_watermarking_technique import wpsnr
from DCT_DWT_SVD_watermarking_technique import detection
from skimage.metrics import structural_similarity
import cv2

from os import listdir
from os.path import isfile, join

def imageOnFolder(mypath) :
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def main():

    imagesToAttack = imageOnFolder('./imagesToAttack/')
    results = []
    thisImageResults = []
    attacksFunctions = [attacks.awgn, attacks.blur, attacks.sharpening, attacks.median, attacks.resizing, attacks.jpeg_compression]
    attacchi = ["awgn", "blur", "sharpening", "median", "resizing", "jpeg_compression"]
    str_arr = [1, 0.5,  1,  1, 1, 90] # parametri partenza
    alpha_arr = [0.5, 0.5, 0.5, 2, -0.5, -5] # incrementi

    for path in imagesToAttack:
        thisImageResults = []
        groupName = path.split('_')[0]
        imageName = path.split('_')[1]
        originalPath = "./originalImages/" + str(imageName)

        if originalPath[-4:] == ".bmp":
            originalPath="./originalImages/" + imageName[:-4]+".jpeg"





        watermarkedPath = "./imagesToAttack/" + str(path)

        print(f'Testing {imageName} of the group {groupName}...')

        # Read image
        watermarked = cv2.imread(watermarkedPath, 0)

        res_att = np.copy(watermarked)
        for c in range(6):  #Dove range(6) indica lo spazio dei possibili attacchi
            wpsnr = 36      #Parametro standard, 36 rappresenta il valore limite oltre il quale l'immagine perde troppa qualità
            found = 1       #Maggiore è il PSNR, migliore è la qualità dell'immagine compressa o ricostruita
            strength = str_arr[c]
            alpha = alpha_arr[c]
            failed_att = 0
            iteration=0
            while found == 1 and wpsnr >= 35 and failed_att == 0:
                strength += alpha
                print(attacks.attack_name(c))
                res_att = attacksFunctions[c](watermarked, strength)
                res_att = np.rint(res_att).astype(int)
                cv2.imwrite('./DCT_DWT_SVD_watermarking_technique/tempImage/tmp.bmp', res_att)
                iteration=iteration + 1

                found, wpsnr =detection.detection(originalPath, watermarkedPath, './DCT_DWT_SVD_watermarking_technique/tempImage/tmp.bmp', imageName, groupName, iteration, attacchi[c] )


                if wpsnr < 35:
                    failed_att = 1
                print("found:"+str(found))
                print("wpsnr:"+str(wpsnr))

                if strength == 0 and c==4:
                    failed_att=1
            if failed_att == 0:
                res = {
                    "imagePath": watermarkedPath,
                    "imageName": imageName,
                    "groupName": groupName,
                    "methodName": attacks.attack_name(c),
                    "methodCode": c,
                    "WPSNR": wpsnr,
                    "params": strength,
                }
                thisImageResults.append(res)
                results.append(res)


        if thisImageResults: # If there is at least one attack
            # Save the images with the best attack
            best_attack = sorted(thisImageResults, key=lambda x:x["WPSNR"])[-1]
            watermarked = cv2.imread(best_attack["imagePath"], 0)
            attackedImage = attacksFunctions[best_attack["methodCode"]](watermarked, best_attack["params"])
            cv2.imwrite('./Testing/AttackedImages/dcexam_' +  best_attack["groupName"] + "_" + best_attack["imageName"], res_att)
            saveThis = [best_attack["imageName"], best_attack["groupName"], best_attack["WPSNR"], f'{best_attack["methodName"]} param: {best_attack["params"]}']
            attacks.append_list_as_row('./Testing/AttackedImages/attacks.csv', saveThis)

    print(results)
    print("\n")
    for res in results:
        print(f'imge: {res["imageName"]}\ngroup: {res["groupName"]}\nmethod: {res["methodName"]}\nWPSNR: {res["WPSNR"]}\nparams: {res["params"]}\n')
import attacks
from embed_panebbianco import *
import functions as f
import detection_panebbianco

imagesToAttack = f.imageOnFolder('../imagesToAttack/')

results = []
thisImageResults = []
attacksFunctions = [attacks.awgn, attacks.blur, attacks.sharpening, attacks.median, attacks.resizing, attacks.jpeg_compression]
str_arr = [1, 0.5,  1,  1, 1, 90] # parametri partenza
alpha_arr = [0.5, 0.5, 0.5, 2, -0.5, -5] # incrementi

for path in imagesToAttack:
    thisImageResults = []
    groupName = path.split('_')[0]
    imageName = path.split('_')[1]
    originalPath = "../originalImages/" + str(imageName)
    watermarkedPath = "../imagesToAttack/" + str(path)
    print(f'Testing {imageName} of the group {groupName}...')

    # Read image
    watermarked = cv2.imread(watermarkedPath, 0)

    res_att = np.copy(watermarked)
    for c in range(6):
        wpsnr = 36
        found = 1
        strength = str_arr[c]
        alpha = alpha_arr[c]
        failed_att = 0
        while found == 1 and wpsnr >= 35 and failed_att == 0:
            strength += alpha
            print(attacks.attack_name(c))
            res_att = attacksFunctions[c](watermarked, strength)
            res_att = np.rint(res_att).astype(int)
            cv2.imwrite('./tempImage/tmp.bmp', res_att)

            found, wpsnr =detection_panebbianco.detection(originalPath, watermarkedPath, './tempImage/tmp.bmp')


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
        cv2.imwrite('../attackedimages/panebbianco_' +  best_attack["groupName"] + "_" + best_attack["imageName"], res_att)
        saveThis = [best_attack["imageName"], best_attack["groupName"], best_attack["WPSNR"], f'{best_attack["methodName"]} param: {best_attack["params"]}']
        attacks.append_list_as_row('../attackedimages/attacks.csv', saveThis)

print(results)
print("\n")
for res in results:
    print(f'imge: {res["imageName"]}\ngroup: {res["groupName"]}\nmethod: {res["methodName"]}\nWPSNR: {res["WPSNR"]}\nparams: {res["params"]}\n')

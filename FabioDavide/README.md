# Obiettivo: Test del codice e interpretazione dei risultati. 
Ci sono due cartelle:
- **DCT_DWT_SVD_watermarking_technique** Link: https://github.com/matteogreek/DCT-DWT-SVD-watermarking-technique
All'interno contiene vari file/cartelle che riguardano gli "attacchi" al watermark, il "check_diffs" che anche noi ci eravamo prefissati, ovvero andare a vedere le differenze tra le immagini e vari indici di test come la "*ROC*" oppure "*wpsnr*", "*threshold*". Inoltre contiene già una cartella con i paper utilizzati per la creazione del progetto, dunque non dovrebbe essere troppo difficile reperire le informazioni teoriche sulle tecniche usate. L'obiettivo in questa cartella è quindi capire tutto il comparto "Attacchi, valutazione, check delle differenze".
- **Robust Watermarking** Link: https://github.com/wheatdog/robust-watermark-against-jpeg
All'interno contiene "embed" ed "extract" che mettono ed estraggono il watermark. La parte relativa ai test e le statistiche sono : "*nc*" e "*psnr*". Sono due tecniche alle quali aggiungerei anche "*ber*". Queste sono appunto 3 tecniche apposite dei watermark per valutare le immagini e il watermark appunto.

Ho caricato la cartella con le varie immagini con e senza watermark. Le immagini sono in formato bmp perchè mi pare che il primo dei due algoritmi lavori con immagini bmp e sono 512x512 perchè mi pare le volesse di questa size. Se avete bisogno di immagini in altro formato e/o size contattatemi.

CheckList:
- [ ] Analisi **DCT_DWT_SVD_watermarking_technique**
- [ ] Analisi **Robust Watermarking**

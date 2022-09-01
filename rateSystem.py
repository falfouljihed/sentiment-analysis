

def rateSystemOutput(results):
    somme = 0
    for result in results:
        print(result)
        if result[0]['label'] == 'LABEL_1':
            somme += 1
    return somme/len(results) * 10
        


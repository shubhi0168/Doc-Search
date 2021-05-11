from PredictPaper import PredictPaper

# Driver Function 
if __name__ == "__main__": 
    dataPath = "drive/My Drive/Colab Notebooks/Data.xlsx"
    graphPath = "drive/My Drive/Colab Notebooks/rake/output2k"
    predPap = PredictPaper(dataPath, graphPath)
    inputKey  = ['cloud computing', 'computer']
    commonWords = 3
    result = predPap.predict(inputKey, commonWords)
    print(result)
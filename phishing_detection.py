import numpy as np
import feature_extraction
from sklearn.ensemble import RandomForestClassifier as rfc
#from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression as lr
from flask import jsonify


def getResult(url):

    #Importing dataset
    data = np.loadtxt("dataset.csv", delimiter = ",")

    #Seperating features and labels
    X = data[: , :-1]
    y = data[: , -1]

    #Seperating training features, testing features, training labels & testing labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    clf = rfc()
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("Score: ",score*100)

    X_new = []

    X_input = url
    data_set,whois_response,rank_checker_response,global_rank,url,domain=feature_extraction.generate_data_set(X_input)
    X_new=data_set
    # X_new=feature_extraction.generate_data_set(X_input)
    X_new = np.array(X_new).reshape(1,-1)
    # print All Details

    print("Whois Response: ", whois_response)
    print("Rank Check", rank_checker_response)
    print("Global Rank: ",global_rank)
    print("URL: ",url)
    print("Domain: ",domain)

    try:
        prediction = clf.predict(X_new)
        if prediction == -1:
            return "Phishing Url",whois_response,rank_checker_response,global_rank,url,domain
        else:
            return "Legitimate Url",whois_response,rank_checker_response,global_rank,url,domain
    except:
        return "Phishing Url",whois_response,rank_checker_response,global_rank,url,domain

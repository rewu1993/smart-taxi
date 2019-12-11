FARE_RANGE = {
    0:"$ 0-10 ",
    1:"$ 10-20 ",
    2:"$ 20-30 ",
    3:"$ 30+ "
}

def cab_assistant(input_feature,clf,neigh,y_train):
    rf_pred = clf.predict(input_feature)[0]
    idcs = neigh.kneighbors(input_feature,n_neighbors = 10, return_distance=False)
    neigh_pred = get_nearest_amount(y_train,idcs)[0]
    median_res = np.median(neigh_pred,-1)
    
    print ('=================================================================')
    print ('Fare Prediction is ', FARE_RANGE[rf_pred])
    print ('Most Similar Historical Fare Records Based on the Input: ')
    print (neigh_pred)
    print ('Historical Fare Records Median: ', median_res)
  
    
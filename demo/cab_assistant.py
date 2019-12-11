from joblib import dump, load

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

def read_tpu_hour():
    sub_chap_num = int(input("Enter the pickup hour (0-24): "))
    if sub_chap_num > 24 or sub_chap_num<0:
        print ('Wrong input, please enter again')
        sub_chap_num = read_tpu_hour()
    return sub_chap_num

def read_puid_hour():
    val = int(input("Enter the pickup location ID (1-263): "))
    if val > 263 or val<1:
        print ('Wrong input, please enter again')
        val = read_puid_hour()
    return val
 
def read_precipitation():
    val = float(input("Enter the precipitation amount (inch): "))
    return val

def read_snow():
    val = float(input("Enter the snow amount (inch): "))
    return val

def read_Tmax():
    val = float(input("Enter the max temperature (F): "))
    return val

def read_Tmin():
    val = float(input("Enter the min temperature (F): "))
    return val


def main():
    clf = load('rf_clf.joblib') 
    neigh = load('kn.joblib') 
    tpu_hour = read_tpu_hour()
    pu_id = read_puid_hour()
    prep = read_precipitation()
    snow = read_snow()
    Tmin = read_Tmin()
    Tmax = read_Tmax()
    input_feature = np.array([tpu_hour,pu_id,prep,snow,Tmax,Tmin]).reshape(-1,6)
    
    cab_assistant(input_feature,clf,neigh,y_train)





    
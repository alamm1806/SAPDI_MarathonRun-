# Example Python script to perform training on input data & generate Metrics & Model Blob
def on_input(data):
    
    # Obtain data
    import pandas as pd
    import io
    df_data = pd.read_csv(io.StringIO(data), sep=";")
    
    # Get predictor and target
    x = df_data[["HALFMARATHON_MINUTES"]]
    y_true = df_data["MARATHON_MINUTES"]
    
    # Train regression
    from sklearn.linear_model import LinearRegression
    lm = LinearRegression()
    lm.fit(x, y_true)
    
    # Model quality
    import numpy as np
    y_pred = lm.predict(x)
    mse = np.mean((y_pred - y_true)**2)
    rmse = np.sqrt(mse)
    rmse = round(rmse, 2)
    
    # to send metrics to the Submit Metrics operator, create a Python dictionary of key-value pairs
    metrics_dict = {"RMSE": str(rmse), "n": str(len(df_data))}
    
    # send the metrics to the output port - Submit Metrics operator will use this to persist the metrics 
    api.send("metrics", api.Message(metrics_dict))

    # create & send the model blob to the output port - Artifact Producer operator will use this to persist the model and create an artifact ID
    import pickle
    model_blob = pickle.dumps(lm)
    api.send("modelBlob", model_blob)
    
api.set_port_callback("input", on_input)
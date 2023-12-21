import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Model
from keras.layers import Input, Dense
from keras.optimizers import Adam


class SpamDetector:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.autoencoder = None
        self.error_threshold = None

    def _build_autoencoder(self, input_dim):
        input_layer = Input(shape=(input_dim,))
        encoded = Dense(128, activation='relu')(input_layer)
        encoded = Dense(64, activation='relu')(encoded)
        decoded = Dense(128, activation='relu')(encoded)
        output_layer = Dense(input_dim, activation='sigmoid')(decoded)

        autoencoder = Model(input_layer, output_layer)
        autoencoder.compile(optimizer=Adam(
            learning_rate=0.001), loss='mean_squared_error')
        return autoencoder

    def train(self, data, epochs=50, batch_size=256):
        data_scaled = self.scaler.fit_transform(data)

        self.autoencoder = self._build_autoencoder(data_scaled.shape[1])
        self.autoencoder.fit(data_scaled, data_scaled,
                             epochs=epochs, batch_size=batch_size, shuffle=True)

        # Determine the reconstruction error threshold
        predictions = self.autoencoder.predict(data_scaled)
        mse = np.mean(np.power(data_scaled - predictions, 2), axis=1)
        # Setting the threshold as the 95th percentile of error
        self.error_threshold = np.percentile(mse, 95)

    def is_spam(self, data_point):
        data_point_scaled = self.scaler.transform([data_point])
        predicted = self.autoencoder.predict(data_point_scaled)
        mse = np.mean(np.power(data_point_scaled - predicted, 2), axis=1)
        # Returns True if data point is likely to be spam
        return mse[0] > self.error_threshold

# Example usage
# Assume 'data' is your preprocessed dataset (as a numpy array)
# detector = SpamDetector()
# detector.train(data)
# is_spam = detector.is_spam(new_data_point)  # new_data_point is a new sample to check

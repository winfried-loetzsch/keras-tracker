from tensorflow.keras.callbacks import Callback
from client import start_training, record_progress


class TrackerCallback(Callback):
    def __init__(self):
        super().__init__()
        self.id = None
        self.c_epoch = -1
        self.n_epochs = 0
        self.n_batches = 0

    def on_train_begin(self, logs=None):
        self.id = start_training(self.params["epochs"], self.params["batch_size"], self.params["samples"])
        self.n_batches = (self.params["samples"] / self.params["batch_size"]) + 1
        self.n_epochs = self.params["epochs"]

    def on_train_end(self, logs=None):
        record_progress(self.id, 100, None)

    def on_train_batch_end(self, batch, logs=None):
        if batch == 0:
            self.c_epoch += 1

        pr = self.c_epoch / self.n_epochs + (1.0 / self.n_epochs) * (batch / self.n_batches)
        record_progress(self.id, int(pr * 100), logs["loss"])
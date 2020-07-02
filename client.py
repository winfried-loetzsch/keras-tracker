import os
import uuid

import requests


def register(client_id, details):
    d_string = ""

    for d in details:
        d_string += str(d) + "</br>"

    requests.post('http://127.0.0.1:5000/register', json={'Id': client_id, 'Details': d_string[:-5]})


def deregister(client_id):
    requests.post('http://127.0.0.1:5000/deregister', json={'Id': client_id})


def progress(client_id, n, status):
    s_string = ""
    progress = "" if n is None else str(n)

    for s in status:
        s_string += str(s) + "</br>"

    if len(s_string) > 0:
        s_string = s_string[:-5]

    requests.post('http://127.0.0.1:5000/status', json={'Id': client_id, 'Progress': progress, 'Status': s_string})


def start_training(epochs, batch_size, samples):
    client_id = str(uuid.uuid1())
    cwd = os.getcwd()

    register(client_id, ["Dir: " + str(cwd),
                         "Number of Epochs: " + str(epochs),
                         "Batch size: " + str(batch_size),
                         "Max i: " + str(samples)])

    return client_id


def record_progress(client_id, progress_percent, loss):
    details = [] if loss is None else ["Avg loss: " + str(loss)]
    progress(client_id, progress_percent, details)

    if progress_percent == 100:
        deregister(client_id)

import csv
import requests
import argparse
from subprocess import Popen, PIPE
from time import sleep


def read_csv_with_header(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header line
        data = []
        for row in reader:
            d = dict(zip(header, row))
            del d["id_"]
            data.append(d)
            # Process the data for each row
    return data

def upload_single(data: dict, url: str):
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print(f"Error uploading data: {response.json()['error']}")
        return None
    return response

def upload_all(data: list, url_master: str, url_helper: str, task_id: str, time_precision: int, vdaf: str, bits: str = "", length: str = "", bins: list = [], variance_task_id: str = ""):
    ids = []
    for i in range(len(data)):
        if vdaf == "sum" or vdaf=="variance":
            json = {
                "measurement": data[i]["age"],
                "task_id": task_id,
                "time_precision": time_precision,
                "vdaf": {"type" : "Prio3Sum",
                        "bits" : bits
                        },
                "leader": url_master,
                "helper": url_helper
                }
        elif vdaf == "vector_sum":
            json = {
                "measurement": data[i],
                "task_id": task_id,
                "time_precision": time_precision,
                "vdaf": {"type" : "Prio3SumVec",
                        "bits" : bits,
                        "length": length
                        },
                "leader": url_master,
                "helper": url_helper
                }
        elif vdaf == "histogram":
            json = {
                "measurement": data[i]["age"],
                "task_id": task_id,
                "time_precision": time_precision,
                "vdaf": {"type" : "Prio3Histogram",
                        "buckets" : bins,
                        },
                "leader": url_master,
                "helper": url_helper
                }
        print(json)
        res = upload_single(json, "http://127.0.0.1:8080/internal/test/upload")
        print(res.json())
        if vdaf == "variance":
            json = {
                "measurement": str(int(data[i]["age"]) ** 2),
                "task_id": variance_task_id,
                "time_precision": time_precision,
                "vdaf": {"type" : "Prio3Sum",
                        "bits" : str(int(bits) * 2) 
                        },
                "leader": url_master,
                "helper": url_helper
                }
            res = upload_single(json, "http://127.0.0.1:8080/internal/test/upload")
            print(res.json())
        if not res:
            return False
    return True

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_filepath', type=str, help='Path to the data file')
    parser.add_argument('master_url', type=str, help='Master URL')
    parser.add_argument('helper_url', type=str, help='Helper URL')
    parser.add_argument('task_id', type=str, help='Task id')
    parser.add_argument('time_precision', type=int, help='Time precision')
    parser.add_argument('vdaf', type=str, help='Metric to calculate')
    parser.add_argument('--bits', type=str, help='bit length for sum')
    parser.add_argument('--length', type=str, help='list length for vector sum')
    parser.add_argument('--bins', type=str, nargs='+', help='bins for histogram')
    parser.add_argument('--vartaskid', type=str, help='variance secondary task id')
    return parser.parse_args()

public_key_master = None
public_key_helper = None

if __name__ == "__main__":

    p = Popen(["./bin/janus_interop_client", "--port", "8080"], shell=True, stdout=PIPE, stderr=PIPE)
    sleep(1)
    print(p.pid)
    args = parse_arguments()
    filepath = args.data_filepath
    master_url = args.master_url
    helper_url = args.helper_url
    task_id = args.task_id
    time_precision = args.time_precision
    vdaf = args.vdaf
    bits = args.bits
    length = args.length
    bins = args.bins
    variance_task_id = args.vartaskid

    print(f"Filepath: {filepath}")
    print(f"Master URL: {master_url}")
    print(f"Helper URL: {helper_url}")
    print(f"Task ID: {task_id}")
    print(f"Time precision: {time_precision}")
    print(f"VDAF: {vdaf}")
    print(f"Bits: {bits}")
    print(f"Length: {length}")
    print(f"Bins: {bins}")
    print(f"Variance task ID: {variance_task_id}")

    data = read_csv_with_header(filepath)
    ids = upload_all(data, master_url, helper_url, task_id, time_precision, vdaf, bits, length, bins, variance_task_id)
    p.kill()
    p.wait()
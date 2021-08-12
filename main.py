import PySimpleGUI as sg
import itertools
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-data_path", default="dummy_data.json")
parser.add_argument("-required_evaluations_path", default="dummy_required_evaluations.json")
parser.add_argument("-results_path", default="results.json")
args = parser.parse_args()

with open(args.data_path) as f:
    data = json.load(f)
with open(args.required_evaluations_path) as f:
    required_results = json.load(f)
try:
    with open(args.results_path) as f:
        results = json.load(f)
    print("Read existing results:")
    for r in results:
        print(r)
        for k in results[r]:
            print("\t", k, ":", results[r][k])
except FileNotFoundError as ex:
    print("Unable to read existing results:", str(ex))
    results = {}

def make_tuple_id(id1, id2):
    return id1 + "_" + id2

def get_next(data, required_results, results):
    """Fetch ids for next comparison"""
    for r in required_results:
        for v in required_results[r]:
            if r not in results:
                results[r] = {}
            if make_tuple_id(*v) not in results[r]:
                return r, v
    return None

def populate_next(window, ref_id, cand_ids, data):
    ref = data[ref_id]
    cands = [data[c] for c in cand_ids]
    window.Element("reference").Update(ref)
    window.Element("candidate1").update(cands[0])
    window.Element("candidate2").update(cands[1])
    window.Element("ref_frame").Update("Reference --  " + ref_id)
    window.Element("cand1_frame").update("Candidate 1 --  " + cand_ids[0])
    window.Element("cand2_frame").update("Candidate 2 --  " + cand_ids[1])

BUTTON_LABELS =  "pick1 pick2".split()
def make_window():
    buttons = [sg.Button(l) for l in BUTTON_LABELS]
    mlref = sg.Multiline("ref", key="reference", disabled=True, size=(166, 10))
    sz = (80, 10)
    mlc1 = sg.Multiline("c1", key="candidate1", disabled=True, size =sz)
    mlc2 = sg.Multiline("c2", key="candidate2", disabled=True, size=sz)
    layout = [
            [sg.Frame(title="reference", key="ref_frame", layout=[[mlref]])], 
            [
                sg.Frame(title=title, key=f"cand{t+1}_frame",layout=[[ml], [buttons[t]]])
                for t, (title, ml) in enumerate(zip("candidate1 candidate2".split(), (mlc1, mlc2)))
            ]
            
        ]
    window = sg.Window("Evaluation", layout)
    window.finalize()
    return window

window = make_window()
res = get_next(data, required_results, results)
if res is None:
    print("Evaluation already complete!")
    exit(0)
current_ref_id, current_cand_ids = res
populate_next(window, current_ref_id, current_cand_ids, data)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"):
        break
    elif event in BUTTON_LABELS:
        picked = current_cand_ids[BUTTON_LABELS.index(event)]
        if current_ref_id not in results:
            results[current_ref_id] = {}
        results[current_ref_id][make_tuple_id(*current_cand_ids)] = picked
        res = get_next(data, required_results, results)
        print("Updating results file.")
        with open("results.json", "w") as f:
            json.dump(results, f)
        if res is None:
            print("Done!")
            break
        current_ref_id, current_cand_ids = res 
        populate_next(window, current_ref_id, current_cand_ids, data)

window.close()
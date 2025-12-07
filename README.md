🔐 NetSec ML Intrusion Detection System

Victim–Attacker Web Demo (Flask + TensorFlow)

This project demonstrates a web‑based cyber attack simulation using a trained Intrusion Detection System (IDS) model.
There are two panels:

Victim Interface — displays the ML detection result

Attacker Interface — allows sending malicious/benign samples to the model

⚙️ Requirements

Python 3.10 (Strict requirement — TensorFlow depends on this)

Windows/macOS/Linux (recommended to store project outside OneDrive to avoid locked file errors)

📦 Installation

1️⃣ Open a terminal and navigate to the backend folder:

cd backend


2️⃣ Create a virtual environment (recommended):

python -m venv venv
venv\Scripts\activate       # Windows
# OR
source venv/bin/activate    # macOS/Linux


3️⃣ Install dependencies from requirements.txt:

pip install -r requirements.txt

🧠 Train the Model (only required once)

Open netsec.ipynb in Jupyter Notebook or VS Code

Run all cells

The notebook will:

Train the DNN model

Save trained files locally into the model_files/ folder:

dnn_cicids2017_model.h5
scaler.gz
label_mapping.pkl


Close the notebook when completed

🚀 Run the Backend Server

Inside the backend folder, run:

py app.py


If successful, you will see:

🚀 Server running: http://127.0.0.1:5000/

🌐 Open the Web Interfaces

Open two tabs in your browser:

URL	Interface	Purpose
http://127.0.0.1:5000
	Victim Panel	Shows predicted attack type
http://127.0.0.1:5000/attacker
	Attacker Panel	Selects sample and triggers prediction
📌 How Samples Work

Samples come from data/samples.xlsx
(numeric features only)

Additional labels (ground truth) are in:
data/samples_label.xlsx

🧮 Index difference note:

Entered Sample Index	Actual Row in File
0 →	Row 2 in Excel
1 →	Row 3
2 →	Row 4
…	…

➡️ This is because row 0 is header, and row 1 is removed during preprocessing.
So the index you type is always 2 rows behind the file’s visible numbering.

👍 You can use samples_label.xlsx to confirm what attack class that row truly is.

📋 Workflow Summary
Step	Action
1️⃣	Install Python 3.10
2️⃣	cd backend & pip install -r requirements.txt
3️⃣	Run notebook netsec.ipynb → saves model
4️⃣	py app.py → start the server
5️⃣	Open Victim & Attacker pages in browser
6️⃣	Use attacker panel to send samples
7️⃣	Victim panel displays IDS prediction
🎯 What You Can Demonstrate
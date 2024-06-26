## DLP Gateway Policy Enforcer

### Overview
The DLP Gateway Policy Enforcer is a tool that allows you to enforce DLP policies on your data in real-time. It is a lightweight, easy-to-use tool that can be deployed in your environment to enforce DLP policies on your data. The DLP Gateway Policy Enforcer is designed to be used in conjunction with your existing DLP solutions to provide an additional layer of protection for your data.

### Authors
- Maor Elfassy
- Efraim Yosofov

### How to run it?
1. Clone the repository
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Import the API and use it for each of your emails
```python
from dlp_gateway.api import classify_mail
email_content = {}
result = classify_mail(email_content)
```


### Policies
#### Policy Group #1 – Internal Data Sharing Limitations and Geo-fencing
- Rule #1 – Legal related emails cannot be transferred between ECT and EES within the corporation 
  - Example: contract discussion between ECT and 3rd party company cannot be sent to EES employee.
- Rule #2 – financial data cannot be transferred between EU and USA 
  - Example: financial reports cannot be transferred between London/EU employee and Houston/NA employee.
- Rule #3 – no business or financial emails/documents can leave corporation perimeter 
  - Example: data on projects cannot be transferred outside Enron Corporation (including all companies)
#### Policy Group #2 – Privacy and Sensitivity
- Rule #1 – emails containing finance information with PII or QID must not leave ECT company. 
  - Example: mail with financial reports with SSN sent from ECT worker to EES worker – must be blocked.
- Rule #2 – sensitive business information can be passed only between VPs, Directors, and C-level employees 
  - Example: project status update regarding future site opening.
- Rule #3 – block mails containing PII or number of QIDs sent outside the corporation. 
  - Example: mail with internal company IP addresses and employee addresses.


### Developer - How to install?
In order to install the spaCy model, you need to run the following command:
```bash
python -m venv .env
source .env/bin/activate
pip3 install -U pip setuptools wheel
pip3 install -U 'spacy[transformers,lookups,apple]'
python3 -m spacy download en_core_web_sm
```
* Read more about the installation of the spaCy model [here](https://spacy.io/usage/models)


###  Files
- `dlp_gateway_policy_enforcer.ipynb` - the main API for the DLP Gateway Policy Enforcer
- `eda.ipynb` - a Jupyter notebook contains our EDA - exploratory data analysis
- `content_analysis_training.ipynb` - a Jupyter notebook contains the template for the DLP Gateway Policy Enforcer that compared between Spacy and Presidio
- `lda_model.ipynb` - a Jupyter notebook contains the LDA model for the DLP Gateway Policy Enforcer
- `bert_model.ipynb` - a Jupyter notebook contains the BERT model for the DLP Gateway Policy Enforcer
- `random_forest.ipynb` - a Jupyter notebook contains the Random Forest model for the DLP Gateway Policy Enforcer
- `preprocessing.py` - a Python script that contains the preprocessing functions for the DLP Gateway Policy Enforcer data

#####  

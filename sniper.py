from flask import Flask, jsonify, render_template_string, request
import numpy as np
import pandas as pd
from functions import processData, subsDefault
import sys


app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run():
    # Get file from the form
    try:
        substrates = request.files.get('textFile')
        loadFile = False
        if substrates:
            loadFile = True

            # Read the contents of the file
            substrate = substrates.read().decode('utf-8')

            # Split the content by lines to get each substrate sequence
            substrates = substrate.splitlines()
        else:
            substrates = subsDefault()

    except Exception as e:
        return jsonify({"error": f"Error A: {str(e)}"}), 400


    # Get other data from the form
    enzymeName = request.form.get('enzymeName')
    entropyMin = request.form.get('entropyMin')
    NSelect = request.form.get('N')
    NSelect = int(NSelect)

    # Evaluate: Data
    dataset = processData(substrates, entropyMin, NSelect, enzymeName, loadFile)

    result = {
        "enzyme": enzymeName,
        "entropyMin": entropyMin,
        "NSelect": NSelect,
        "NBinSubs": dataset['NBinSubs'],
        "figProb": dataset['probability'],
        "figEntropy": dataset['entropy'],
        "figLogo": dataset['pLogo'],
        "barCounts": dataset['barCounts'],
        "barProb": dataset['barProb'],
        "figWords": dataset['words']
    }

    return jsonify(result)


@app.route('/')
def home():
    return render_template_string('''
    <html>
        <head>
            <title>SNIPER</title>
            <style>
                body {
                    background-color: {{ black }};
                    color: #f0f0f0;
                    font-family: Arial, sans-serif;
                    padding: 40px;
                }
                h1 {
                    text-align: center;
                    font-size: 35px;
                    padding: 0px;
                }
                h2 {
                    text-align: center;
                    font-size: 25px;
                    padding: 10px;
                }
                p {
                    font-size: {{ fontSize }}px;
                    text-align: center;
                    padding-top: 0px;
                    padding-bottom: 0px;
                }
                .container-description {
                    background-color: {{ grey }};
                    color: {{ white }};
                    font-size: 20px;
                    text-align: center;
                    border-radius: {{ borderRad }}px;
                    line-height: 1.4;
                    margin: 20px auto;
                    padding: 20px;
                }
                .container {
                    background-color: {{ grey }};
                    font-size: 20px;
                    text-align: center;
                    border-radius: {{ borderRad }}px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: {{ padTB }}px {{ padSide }}px {{ marginB }}px {{ padSide }}px;
                    margin: {{ spacer }}px auto;
                    margin-bottom: {{ marginB }}px;
                }
                .container-input {
                    background-color: {{ grey }};
                    font-size: 20px;
                    text-align: center;
                    border-radius: {{ borderRad }}px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 0px 0px 0px 0px;
                    margin: {{ spacer }}px auto;
                    margin-bottom: {{ marginB }}px;
                }
                .container-params {
                    background-color: {{ grey }};
                    font-size: 20px;
                    border-radius: {{ borderRad }}px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    line-height: 0.01;
                    padding: 0px 0px 0px 0px;
                    margin: 5px auto;
                }
                .container-figDescription {
                    font-size: 18px;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 5px 0px 0px 0px;
                    margin: 0px auto;
                }
                .container-fig {
                    background-color: {{ grey }};
                    font-size: 20px;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 50px 0px 0px 0px;
                    margin: 5px auto;
                    margin-top: 0px
                }
                .container-fig img {
                    margin-top: 0px;
                }
                .div-header {
                    color: {{ green }};
                    font-size: 22px;
                    font-weight: normal;
                    padding-top: 0px;
                    padding-bottom: 5px;
                }
                input[type="file"] {
                    background-color: {{ black }};
                    color: #101010;
                    font-size: {{ fontSize }}px;
                    border: 2px solid {{ greyDark }};
                    border-radius: {{ borderRad }}px;
                    width: 100%;
                    max-width: 350px;
                    padding: {{ padInput }}px;
                    margin-bottom: {{ padTB }}px;
                }
                button {
                    background-color: {{ green }};
                    color: {{ white }};
                    font-size: {{ fontSize }}px;
                    cursor: pointer;
                    border: none;
                    border-radius: {{ borderRad }}px;
                    padding: 8px 20px;
                    margin-top: {{ marginButton }}px;
                    margin-bottom: {{ marginButton }}px;
                }
                button:hover {
                    background-color: {{ greenHighlight }};
                }
                .input-form {
                    align-items: center;
                    text-align: center; /* center form text */
                    display: flex;
                    flex-direction: column;
                    font-size: {{ fontSize }}px;
                }
                .form-group {
                    width: 100%;
                    max-width: 350px;
                    line-height: 1.5;
                }
                .form-group label {
                    display: block;
                    margin-bottom: {{ spacerMini }}px;
                    font-size: {{ fontSize }}px;
                    text-align: center;
                }
                .form-group input {
                    font-size: {{ fontSize }}px;
                    border-radius: {{ borderRad }}px;
                    border: 2px solid {{ greyDark }};
                    text-align: center;
                    width: 100%;
                    padding: {{ padInput }}px;
                    margin-bottom: {{ spacer }}px;
                }
            </style>
        </head>
        <script>
            function evaluateForm(event) {
                event?.preventDefault(); // Prevent any default form action
        
                const enzymeName = document.getElementById('enzymeName').value;
                const entropyMin = document.getElementById('entropyMin').value;
                const N = document.getElementById('N').value;
                const textFileInput = document.querySelector('input[name="textFile"]');
                const textFile = textFileInput.files[0];
        
                if (!enzymeName || !entropyMin || !N) {
                    alert("Please fill out all required fields.");
                    return;
                }
                const formData = new FormData();
                formData.append('enzymeName', enzymeName);
                formData.append('entropyMin', entropyMin);
                formData.append('N', N);
                if (textFile) {
                    formData.append('textFile', textFile);
                }
                fetch('/run', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) throw new Error("Network response was not ok");
                    return response.json();
                })
                .then(data => {
                    const newDiv = document.createElement('div');
                    newDiv.className = 'container';
                    Object.assign(newDiv.style, {
                        backgroundColor: "{{ grey }}",
                        fontSize: "20px",
                        textAlign: "center",
                        borderRadius: "{{ borderRad }}px",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        padding: "{{ padTB }}px {{ padSide }}px {{ padTB }}px {{ padSide }}px",
                        padding: "{{ padTB }}px {{ padSide }}px {{ padTB }}px {{ padSide }}px",
                        margin: "{{ spacer }}px auto",
                        marginBottom: "{{ marginB }}px"
                    });
                    newDiv.innerHTML = `
                        <div class="div-header">Results:</div>
                        <div class=container-params>
                            <p><strong>Enzyme:</strong> ${enzymeName}</p>
                            <p><strong>Min Entropy:</strong> ${entropyMin}</p>
                            <p><strong>Selecting Substrates:</strong> ${data.NBinSubs}</p>
                            <p><strong>Unique Motifs Obtained:</strong> ${data.NBinSubs}</p>
                        </div>
                        <div class=container-fig>
                            <div class="div-header">
                                Amino Acid Probability Distribution:
                            </div>
                            <p><img src="data:image/png;base64,${data.figProb}" 
                                alt="Probability Plot" style="max-width: 100%;" /></p>
                        </div>
                        <div class=container-fig>
                            <div class="div-header">
                                Positional Entropy (ΔS):
                            </div>
                             <div class=container-figDescription>
                                <p>{{ equation|safe }}</p>
                             </div>
                            <p><img src="data:image/png;base64,${data.figEntropy}" 
                                alt="Entropy Plot" style="max-width: 100%;" /></p>
                        </div>
                        <div class=container-fig> 
                            <div class="div-header">
                                    pLogo:
                                </div>
                                <div class=container-figDescription>
                                    <p>Letter Size = ΔS<sub>Pos</sub> × 
                                        prob<sub>AA@Pos</sub></p>
                                 </div>
                            <p><img src="data:image/png;base64,${data.figLogo}" 
                                alt="pLogfo" style="max-width: 100%;" /></p>
                        </div>
                        <div class=container-fig> 
                            <div class="div-header">
                                    Substrate Motif:
                            </div>

                            <div class=container-figDescription>
                                <p>Motif Counts:</p>
                            </div>
                            <p><img src="data:image/png;base64,${data.barCounts}" 
                                alt="Bar Graph: Motif Counts" 
                                style="max-width: 100%;" /></p>
                        </div>
                        <div class=container-fig> 
                            <div class=container-figDescription>
                                <p>Motif Probability:</p>
                            </div>
                            <p><img src="data:image/png;base64,${data.barProb}" 
                                alt="Bar Graph: Motif Probability" 
                                style="max-width: 100%;" /></p>
                        </div>
                        <div class=container-fig> 
                            <div class=container-figDescription>
                                <p>Word Cloud:</p>
                            </div>
                            <p><img src="data:image/png;base64,${data.figWords}" 
                                alt="pLogfo" style="max-width: 100%;" /></p>
                        </div>
                    `;
                    document.body.appendChild(newDiv);
                })
                .catch(error => {
                    console.error('Error:', error);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'container';
                    errorDiv.innerHTML = `<p style="color: red;">
                        Error fetching results: ${error.message}</p>`;
                    document.body.appendChild(errorDiv);
                });
            }
        </script>
        <body>
            <h1>{{ title|safe }}</h1>
            <div class="container-description">
                <div class="div-header">Description:</div>
                <p>{{ pg1|safe }}</p>
                <p>{{ pg2|safe }}</p>
                <p>{{ equation|safe }}</p>
                <p>{{ pg3|safe }}</p>
                <p>{{ pg4|safe }}</p>
                <p>{{ pg5|safe }}</p>
            </div>
            <div class="container">
                <div class="container-input">
                    <form action="/run" method="POST" enctype="multipart/form-data" class="input-form">
                    <div class="div-header">Upload Text File:</div>
                    <div class="form-group">
                        <label for="textFile">Uploaded files must be formatted as .txt</label>
                        <input type="file" id="textFile" name="textFile" accept=".txt" class="input-form">
                    </div>

                    <div class="div-header">Experiment Parameters:</div>
                    <div class="form-group">
                        <label for="enzymeName">Name Your Enzyme:</label>
                        <input type="text" id="enzymeName" name="enzymeName" required value=Protease>
                    </div>
                    
                    <div class="form-group">
                        <label for="entropyMin">Minimum Entropy Score:</label>
                        <input type="number" id="entropyMin" name="entropyMin" step="0.1" value="0.6" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="N">Select & Bin "N" Substrates:</label>
                        <input type="number" id="N" name="N" value="25" required>
                    </div>
                        <button type="button" onclick="evaluateForm()">Submit</button>
                    </form>
            </div>
        </body>
    </html>
    ''',
    black='#151515', white='FFFFFF',
    grey='#303030', greyDark='#202020',
    green='#23FF55', greenHighlight='#1AD747',
    spacer=20, spacerMini=5,
    padSide=50, padTB=30, padInput=8,
    marginB=12, marginButton=12,
    fontSize=16,
    borderRad=5,
    title="Specificity Network Identification via Positional Entropy based Refinement "
          "(SNIPER)",
    pg1="This program will take substrates for a given enzyme and identify the "
        "Motif, of the recognition sequence within the larger protein sequence. "
        "The Motif is identified by the positions in the substrate that have "
        "Entropy scores (∆S) that exceed a entropyMin value.",
    pg2="∆S is evaluated at each position in the substrate sequence and is found by "
        "the difference between the Maximum Entropy (S<sub>Max</sub>) and the "
        "Shannon Entropy (S<sub>Shannon</sub>)",
    equation="∆S = S<sub>Max</sub> - S<sub>Shannon</sub> = log<sub>2</sub>(20) - "
            "∑(-prob<sub>AA</sub> * log<sub>2</sub>(prob<sub>AA</sub>))",
    pg3="Once we have identified the Motif, we can bin the substrates to select the only"
        "the recognition sequence. In other words, we remove the parts of the substrate "
        "that are not important for an Enzyme-Substrate interaction.",
    pg4="We can count the occurrences of each Motif, and plot this data in a Bar Graph, "
        "and a Word Cloud. This allows us to display the optimal combinations of amino "
        "acids that fit into the enzymes active site."
        "will plot the and use them as input for a Suffix Tree. This will plot the "
        "preferred residues in descending order of Specificity, as determined by the "
        "∆S values.",
    pg5="We can further evaluate the Motif by feeding the data into a Suffix Tree. "
        "This will reveal the Specificity Network of your enzyme, or the specific "
        "connections between the preferences for a given amino acid when another is "
        "present."
)



if __name__ == '__main__':
    app.run(debug=True)

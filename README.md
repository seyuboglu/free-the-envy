# Criteria of Fairness in Rent Splitting
By: Sabri Eyuboglu, Kye Kim, and KiJung Park

Implementation of the fair-rent splitting algorithms described in the paper [Criteria of Fairness in Rent Splitting](manuscript.pdf).

## Installation
Clone the repository
```
git clone https://github.com/seyuboglu/free-the-envy.git
cd free-the-envy

```

Create a virtual environment and activate it
```
python3 -m venv ./env
source env/bin/activate
```

Install required python packages
```
pip install -r requirements.txt
```

## Launching the Web Interface 
Launch the interface with
```
python src/js_io.py 
```
and open the link in your browswer. 


## Computing Standalone Splits
First make directory for your split and create a params json file. 
```
mkdir my_rent_split
cd my_rent_split
vi params.json
```

Write parameters in the following format
```json
{
    "n": 3,
    "total_rent": 5100,

    "methods": ["PriorityMethod",],

    "agent_to_valuations": {
        "Esteban": [1909, 1887, 1304],
        "Irene":  [1700, 1898, 1502],
        "Mark":   [1502, 1836, 1762]
    }, 
}
```
For the `methods` attribute, include a list of rent division methods to run. 

To run them use
```
python src/cli.py --dir my_rent_split --process split_cli
```

The results for each method will be output to console and also written to a csv in the split directory

## Running Simulations
To run a simulation of many synthetic rent-splitting instances

Our simulations generate random rent-splitting instances using nested dirichlet distributions. 
```json
{
    "methods":  ["PriorityMethod"],
    "n": 5,
    "num_samples": 10000,

    "x_scale": "log",

    "mean_scale": 0.5,
    "initial_scale": 10
}
```

## Analyzing User Study Data
Create a directory for the survey 
```
mkdir survey
cd survey
```

Add survey data as a csv to a data subdir directory. 
```
mkdir data
```

Each survey question should be a separate CSV, with a row for each response and column for each option and other metadata.

Create a parameters json file
```
vi params.json
```
and specify parameters in the following format 

```
{
    "questions": {
        "utility_v_demand.csv": 
            {
                "options": ["utility", "demand"],
                "target": "demand",
                "plots": ["group_plot"]
            }, 
        "utility_v_price.csv":
            {
                "options": ["utility", "price"],
                "target": "price",
                "plots": []

            }
    }

}
```



``

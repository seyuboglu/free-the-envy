"""
"""
import os

import numpy as np
from scipy.stats import binom_test
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import Process

class SurveyResults(Process):
    """
    """
    def __init__(self, params):
        super().__init__(params)

        self.question_dfs = {}
        for question_file in self.questions.keys():
            path = os.path.join(self.dir, "data", question_file)
            self.question_dfs[question_file] = pd.read_csv(path)
    
    def run(self):
        for question_file in self.questions.keys():
            self.binomial_test(question_file)
        
        for question_file in self.questions.keys():
            params = self.questions[question_file]
            for plot_method in params["plots"]:
                getattr(self, plot_method)(question_file)

    def binomial_test(self, question):
        """
        """
        params = self.questions[question]
        df = self.question_dfs[question]

        counts = {option: np.sum(df[option]) for option in params["options"]}

        total = np.sum(list(counts.values()))

        print(counts)
        print(binom_test(counts[params["target"]], total, p=1 / len(params["options"])))
    
    def group_plot(self, question):
        df = self.question_dfs[question]
        #plot = sns.countplot(x="house", hue="choice", data=df)
        plot = sns.barplot(x="house", y="house", hue="choice", data=df, estimator=lambda x: len(x) / len(df) * 100, orient="v")
        plt.savefig(os.path.join(self.dir, "group_plot.pdf"))


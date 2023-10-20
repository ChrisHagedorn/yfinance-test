import lzma
import pickle
import pandas as pd
import numpy as np

def load_pickle(path):
    with lzma.open(path, "rb") as fp:
        file = pickle.load(fp)
    return file

def save_pickle(path, obj):
    with lzma.open(path, "wb") as fp:
        pickle.dump(obj, fp)


class Alpha():
    def __init__(self, insts, dfs, start, end):
        self.insts = insts
        self.dfs = dfs
        self.start = start
        self.end = end

    def init_portfolio_settings(self, trade_range):
        portfolio_df = pd.DataFrame(index=trade_range).reset_index()
        portfolio_df = portfolio_df.rename(columns={"index": "datetime"})
        portfolio_df.loc[0, "capital"] = 10000
        return portfolio_df
    
    def compute_meta_info(self, trade_range):
        for inst in self.insts:
            df = pd.DataFrame(index=trade_range)
            self.dfs[inst] = df.join(self.dfs[inst]).fillna(method="ffill").fillna(method="bfill")
            self.dfs[inst]["ret"] = -1 + self.dfs[inst]["close"]/self.dfs[inst]["close"].shift(1) #give daily return
            sampled = self.dfs[inst]["close"] != self.dfs[inst]["close"].shift(1).fillna(method="bfill")
            eligible = sampled.rolling(5).apply(lambda x: int(np.any(x))).fillna(0)
            self.dfs[inst]["eligible"] = eligible.astype(int) & (self.dfs[inst]['close'] >  0).astype(int) #filter for non-0 price stocks
        return
            


    def run_simulation(self):
        print('running backtest')
        date_range = pd.date_range(start=self.start, end=self.end, freq="D")
        self.compute_meta_info(trade_range=date_range)
        portfolio_df = self.init_portfolio_settings(trade_range=date_range)
        for i in portfolio_df.index:
            date = portfolio_df.loc[i, "datetime"]

            eligibles = [inst for inst in self.insts if self.dfs[inst].loc[date, "eligible"]]
            non_eligibles = [inst for inst in self.insts if inst not in eligibles]

            if i != 0:
                
                pass

            # compute alpha signals
            alpha_scores = {}

            # compute positions and other information

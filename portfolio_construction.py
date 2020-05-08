import pandas as pd


class OptimisationPortfolioConstructionModel():

    def __init__(self):
        pass

    def GenerateOptimalPortfolio(self, algorithm, alpha_df):
        # algorithm.Log("Generating target portfolio...")
        
        alpha_portfolio = self.CalcAlphaPortfolio(algorithm, alpha_df)
        
        optimal_portfolio = self.Optimise(algorithm, self.AddZeroHoldings(algorithm, alpha_portfolio))
        
        # algorithm.Log(f"Created a portfolio of {len(optimal_portfolio[optimal_portfolio != 0])} securities (liquidating {len(optimal_portfolio[optimal_portfolio == 0])} securities)")
        
        return optimal_portfolio

    def CalcAlphaPortfolio(self, algorithm, alpha_df):
        portfolio = alpha_df['alpha_score']
        portfolio.name = 'weight'
        port_sum = portfolio.abs().sum()
        if port_sum != 1:
            # algorithm.Log(f"Alpha scores don't add up to 1: {port_sum}")
            portfolio /= port_sum
        return portfolio

    def AddZeroHoldings(self, algorithm, portfolio):
        zero_holding_securities = [s.Symbol for s in algorithm.Portfolio.Values if s.Invested and s.Symbol not in portfolio.index]
        for security in zero_holding_securities:
            portfolio.loc[str(security)] = 0
        return portfolio
    
    def Optimise(self, algorithm, portfolio):
        return portfolio
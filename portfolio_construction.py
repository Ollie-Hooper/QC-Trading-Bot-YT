import pandas as pd
import numpy as np
import cvxpy as cv


class OptimisationPortfolioConstructionModel():

    def __init__(self, turnover, max_wt, longshort):
        self.turnover = turnover
        self.max_wt = max_wt
        self.longshort = longshort

    def GenerateOptimalPortfolio(self, algorithm, alpha_df):
        # algorithm.Log("Generating target portfolio...")
        
        alphas = alpha_df['alpha_score']
        
        optimal_portfolio = self.Optimise(algorithm, self.AddZeroHoldings(algorithm, alphas))
        
        # algorithm.Log(f"Created a portfolio of {len(optimal_portfolio[optimal_portfolio != 0])} securities")
        
        return optimal_portfolio

    def AddZeroHoldings(self, algorithm, portfolio):
        zero_holding_securities = [str(s.Symbol) for s in algorithm.Portfolio.Values if s.Invested and str(s.Symbol) not in portfolio.index]
        for security in zero_holding_securities:
            portfolio.loc[security] = 0
        return portfolio
    
    def Optimise(self, algorithm, alphas):
        invested_securities = [security for security in algorithm.Portfolio.Values if security.Invested]
        if len(invested_securities) == 0:
            algorithm.Log('Initial portfolio rebalance')
            self.initial_rebalance = True
            turnover = 1
            initial_portfolio = pd.DataFrame(columns=['symbol', 'weight', 'alpha']).set_index('symbol')
        else:
            self.initial_rebalance = False
            turnover = self.turnover
            initial_portfolio = pd.DataFrame.from_records(
                [
                    {
                        'symbol': str(security.Symbol),
                        'weight': security.HoldingsValue / algorithm.Portfolio.TotalHoldingsValue,
                        'alpha': alphas.loc[security] if security in alphas.index else 0,
                    } for security in invested_securities
                ]).set_index('symbol')
        for security, alpha in alphas.iteritems():
            if security not in initial_portfolio.index:
                initial_portfolio.loc[security, 'weight'] = 0
                initial_portfolio.loc[security, 'alpha'] = alpha
        
        for i in range(int(turnover*100), 101, 1):
            to = i / 100
            optimiser = Optimiser(initial_portfolio, turnover=to, max_wt=self.max_wt)
            optimal_portfolio, optimisation_status = optimiser.optimise()
            if optimisation_status != 'optimal':
                algorithm.Log(f'Optimisation with {to} turnover not feasible: {optimisation_status}')
            else:
                break
        return optimal_portfolio


class Optimiser:

    def __init__(self, initial_portfolio, turnover, max_wt, longshort=True):
        self.symbols = np.array(initial_portfolio.index)
        self.init_wt = np.array(initial_portfolio['weight'])
        self.opt_wt = cv.Variable(self.init_wt.shape)
        self.alpha = np.array(initial_portfolio['alpha'])
        self.longshort = longshort
        self.turnover = turnover
        self.max_wt = max_wt
        if self.longshort:
            self.min_wt = -self.max_wt
            self.net_exposure = 0
            self.gross_exposure = 1
        else:
            self.min_wt = 0
            self.net_exposure = 1
            self.gross_exposure = 1

    def optimise(self):
        constraints = self.get_constraints()
        optimisation = cv.Problem(cv.Maximize(cv.sum(self.opt_wt*self.alpha)), constraints)
        optimisation.solve()
        status = optimisation.status
        if status == 'optimal':
            optimal_portfolio = pd.Series(np.round(optimisation.solution.primal_vars[list(optimisation.solution.primal_vars.keys())[0]], 3), index=self.symbols)
        else:
            optimal_portfolio = pd.Series(np.round(self.init_wt, 3), index=self.symbols)
        return optimal_portfolio, status

    def get_constraints(self):
        min_wt = self.opt_wt >= self.min_wt
        max_wt = self.opt_wt <= self.max_wt
        turnover = cv.sum(cv.abs(self.opt_wt-self.init_wt)) <= self.turnover*2
        net_exposure = cv.sum(self.opt_wt) == self.net_exposure
        gross_exposure = cv.sum(cv.abs(self.opt_wt)) <= self.gross_exposure
        return [min_wt, max_wt, turnover, net_exposure, gross_exposure]
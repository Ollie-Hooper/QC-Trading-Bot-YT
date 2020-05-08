from universe_selection import FactorUniverseSelectionModel
from alpha_model import ValueAlphaModel
from portfolio_construction import OptimisationPortfolioConstructionModel
from execution import Execution

class TradingBot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2003, 1, 1)
        self.SetCash(100000)
        
        # Data resolution
        self.UniverseSettings.Resolution = Resolution.Minute
        
        # Universe selection model
        self.securities = []
        self.CustomUniverseSelectionModel = FactorUniverseSelectionModel(self)
        self.AddUniverse(self.CustomUniverseSelectionModel.SelectCoarse, self.CustomUniverseSelectionModel.SelectFine)
        
        # Alpha model
        self.CustomAlphaModel = ValueAlphaModel()
        
        # Portfolio construction model
        self.CustomPortfolioConstructionModel = OptimisationPortfolioConstructionModel()
        
        # Execution model
        self.CustomExecution = Execution()
        
        # Add SPY for trading days data
        self.AddEquity('SPY', Resolution.Daily)
        
        # Schedule rebalancing
        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.At(13, 0), Action(self.RebalancePortfolio))

    def OnData(self, data):
        pass
    
    def RebalancePortfolio(self): 
        alpha_df = self.CustomAlphaModel.GenerateAlphaScores(self, self.securities)
        portfolio = self.CustomPortfolioConstructionModel.GenerateOptimalPortfolio(self, alpha_df)
        self.CustomExecution.ExecutePortfolio(self, portfolio)
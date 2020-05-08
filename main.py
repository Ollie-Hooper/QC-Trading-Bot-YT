from universe_selection import FactorUniverseSelectionModel
from alpha_model import ValueAlphaModel
from portfolio_construction import OptimisationPortfolioConstructionModel
from execution import Execution
from charting import InitCharts, PlotPerformanceChart, PlotPosConcentrationChart

class TradingBot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2003, 1, 1)
        self.SetEndDate(2003, 1, 10)
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
        
        # Init charting
        InitCharts(self)
        
        # Schedule charting
        self.Schedule.On(self.DateRules.Every(DayOfWeek.Friday), self.TimeRules.BeforeMarketClose('SPY', 0), Action(self.PlotCharts))

    def OnData(self, data):
        pass
    
    def RebalancePortfolio(self): 
        alpha_df = self.CustomAlphaModel.GenerateAlphaScores(self, self.securities)
        portfolio = self.CustomPortfolioConstructionModel.GenerateOptimalPortfolio(self, alpha_df)
        self.CustomExecution.ExecutePortfolio(self, portfolio)
    
    def PlotCharts(self):
        PlotPerformanceChart(self)
        PlotPosConcentrationChart(self)
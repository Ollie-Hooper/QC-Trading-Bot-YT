from universe_selection import FactorUniverseSelectionModel
from alpha_model import ValueAlphaModel
from portfolio_construction import OptimisationPortfolioConstructionModel
from execution import Execution
from charting import InitCharts, PlotPerformanceChart, PlotPosConcentrationChart, PlotStockCountChart, PlotExposureChart

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
        self.CustomPortfolioConstructionModel = OptimisationPortfolioConstructionModel(turnover=0.05, max_wt=0.05, longshort=True)
        
        # Execution model
        self.CustomExecution = Execution(liq_tol=0.005)
        
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
        PlotStockCountChart(self)
        PlotExposureChart(self)
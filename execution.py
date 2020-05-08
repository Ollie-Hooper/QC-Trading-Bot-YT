class Execution():
    
    def __init__(self):
        pass
    
    def ExecutePortfolio(self, algorithm, portfolio):
        # algorithm.Log(f"Executing portfolio trades...")
        
        liquidate_securities = portfolio[portfolio == 0].index
        holding_port = portfolio[portfolio != 0]
        
        self.LiquidateSecurities(algorithm, liquidate_securities)
        
        self.SetPortfolioHoldings(algorithm, holding_port)
    
    def LiquidateSecurities(self, algorithm, securities):
        # algorithm.Log(f"Liquidating {len(securities)} securities...")
        for security in securities:
            algorithm.Liquidate(security)
        # algorithm.Log(f"Successfully liquidated {len(securities)} securities")
    
    def SetPortfolioHoldings(self, algorithm, portfolio):
        # algorithm.Log(f"Setting portfolio holdings for {len(portfolio)} securities...")
        for security, weight in portfolio.iteritems():
            algorithm.SetHoldings(security, weight)
        # algorithm.Log(f"Successfully set all holdings")
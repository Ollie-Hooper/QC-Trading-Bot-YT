class Execution():
    
    def __init__(self, liq_tol):
        self.liq_tol = liq_tol
    
    def ExecutePortfolio(self, algorithm, portfolio):
        # algorithm.Log(f"Executing portfolio trades...")
        
        liquidate_securities = portfolio[abs(portfolio) < self.liq_tol].index
        holding_port = portfolio[abs(portfolio) >= self.liq_tol]
        
        self.LiquidateSecurities(algorithm, liquidate_securities)
        
        self.SetPortfolioHoldings(algorithm, holding_port)
    
    def LiquidateSecurities(self, algorithm, securities):
        liquid_count = 0
        for security in securities:
            if algorithm.Securities[security].Invested:
                algorithm.Liquidate(security)
                liquid_count += 1
        # algorithm.Log(f"Successfully liquidated {liquid_count} securities")
    
    def SetPortfolioHoldings(self, algorithm, portfolio):
        # algorithm.Log(f"Setting portfolio holdings for {len(portfolio)} securities...")
        for security, weight in portfolio.iteritems():
            algorithm.SetHoldings(security, weight)
        # algorithm.Log(f"Successfully set all holdings")
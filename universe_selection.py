class FactorUniverseSelectionModel():
    
    def __init__(self, algorithm):
        self.algorithm = algorithm
    
    def SelectCoarse(self, coarse):
        # self.algorithm.Log("Generating universe...")
        universe = self.FilterDollarPriceVolume(coarse)
        return [c.Symbol for c in universe]

    def SelectFine(self, fine):
        universe = self.FilterFactor(self.FilterFinancials(fine))
        # self.algorithm.Log(f"Universe consists of {len(universe)} securities")
        self.algorithm.securities = universe
        return [f.Symbol for f in universe]
    
    def FilterDollarPriceVolume(self, coarse):
        filter_dollar_price = [c for c in coarse if c.Price > 1]
        sorted_dollar_volume = sorted([c for c in filter_dollar_price if c.HasFundamentalData], key=lambda c: c.DollarVolume, reverse=True)
        return sorted_dollar_volume[:1000]

    def FilterFinancials(self, fine):
        filter_financials = [f for f in fine if f.AssetClassification.MorningstarSectorCode != MorningstarSectorCode.FinancialServices]
        return filter_financials
    
    def FilterFactor(self, fine):
        filter_factor = sorted(fine, key=lambda f: f.ValuationRatios.CashReturn, reverse=True)
        return filter_factor[:50] + filter_factor[-50:]
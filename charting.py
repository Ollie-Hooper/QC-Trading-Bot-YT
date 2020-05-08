def InitCharts(algorithm):
    performance_plot = Chart('Performance Breakdown')
    performance_plot.AddSeries(Series('Total Fees', SeriesType.Line, 0))
    performance_plot.AddSeries(Series('Total Gross Profit', SeriesType.Line, 0))
    algorithm.AddChart(performance_plot)
    
    concentration_plot = Chart('Position Concentration')
    concentration_plot.AddSeries(Series('Largest Long Position', SeriesType.Line, 0))
    concentration_plot.AddSeries(Series('Largest Short Position', SeriesType.Line, 0))
    concentration_plot.AddSeries(Series('Smallest Long Position', SeriesType.Line, 0))
    concentration_plot.AddSeries(Series('Smallest Short Position', SeriesType.Line, 0))
    algorithm.AddChart(concentration_plot)
    
    stock_count_plot = Chart('Stock Count')
    stock_count_plot.AddSeries(Series('Long', SeriesType.Line, 0))
    stock_count_plot.AddSeries(Series('Short', SeriesType.Line, 0))
    algorithm.AddChart(stock_count_plot)
    
    exposure_plot = Chart('Exposure/Leverage')
    exposure_plot.AddSeries(Series('Gross', SeriesType.Line, 0))
    exposure_plot.AddSeries(Series('Net', SeriesType.Line, 0))
    algorithm.AddChart(exposure_plot)


def PlotPerformanceChart(algorithm):
    algorithm.Plot('Performance Breakdown', 'Total Fees', algorithm.Portfolio.TotalFees)
    algorithm.Plot('Performance Breakdown', 'Total Gross Profit', algorithm.Portfolio.TotalProfit)


def PlotPosConcentrationChart(algorithm):
    long_max_val = 0
    short_max_val = 0
    long_min_val = 999999999
    short_min_val = 999999999
    for security, v in algorithm.Portfolio.items():
        if v.Invested:
            val = v.AbsoluteHoldingsValue
            if v.IsLong:
                if val > long_max_val:
                    long_max_val = val
                if val < long_min_val:
                    long_min_val = val
            elif v.IsShort:
                if val > short_max_val:
                    short_max_val = val
                if val < short_min_val:
                    short_min_val = val
            
    total_holdings = algorithm.Portfolio.TotalHoldingsValue
    long_max_pos = long_max_val / total_holdings
    short_max_pos = short_max_val / total_holdings
    long_min_pos = long_min_val / total_holdings
    short_min_pos = short_min_val / total_holdings
    algorithm.Plot('Position Concentration', 'Largest Long Position', long_max_pos)
    algorithm.Plot('Position Concentration', 'Largest Short Position', short_max_pos)
    algorithm.Plot('Position Concentration', 'Smallest Long Position', long_min_pos)
    algorithm.Plot('Position Concentration', 'Smallest Short Position', short_min_pos)


def PlotStockCountChart(algorithm):
    long_count = 0
    short_count = 0
    for security, v in algorithm.Portfolio.items():
        if v.Invested:
            val = v.AbsoluteHoldingsValue
            if v.IsLong:
                long_count += 1
            elif v.IsShort:
                short_count += 1
    
    algorithm.Plot('Stock Count', 'Long', long_count)
    algorithm.Plot('Stock Count', 'Short', short_count)


def PlotExposureChart(algorithm):
    long_val = 0
    short_val = 0
    for security, v in algorithm.Portfolio.items():
        if v.Invested:
            val = v.AbsoluteHoldingsValue
            if v.IsLong:
                long_val += val
            elif v.IsShort:
                short_val += val
    
    total_equity = algorithm.Portfolio.TotalPortfolioValue
    gross = (long_val + short_val) / total_equity
    net = (long_val - short_val) / total_equity
    algorithm.Plot('Exposure/Leverage', 'Gross', gross)
    algorithm.Plot('Exposure/Leverage', 'Net', net)
def InitCharts(algorithm):
    performance_plot = Chart('Performance Breakdown')
    performance_plot.AddSeries(Series('Total Fees', SeriesType.Line, 0))
    performance_plot.AddSeries(Series('Total Gross Profit', SeriesType.Line, 0))
    algorithm.AddChart(performance_plot)
    
    concentration_plot = Chart('Position Concentration')
    concentration_plot.AddSeries(Series('Largest Long Position', SeriesType.Line, 0))
    concentration_plot.AddSeries(Series('Largest Short Position', SeriesType.Line, 0))
    algorithm.AddChart(concentration_plot)


def PlotPerformanceChart(algorithm):
    algorithm.Plot('Performance Breakdown', 'Total Fees', algorithm.Portfolio.TotalFees)
    algorithm.Plot('Performance Breakdown', 'Total Gross Profit', algorithm.Portfolio.TotalProfit)


def PlotPosConcentrationChart(algorithm):
    long_max_val = 0
    short_max_val = 0
    for security, v in algorithm.Portfolio.items():
        if v.Invested:
            val = v.AbsoluteHoldingsValue
            if v.IsLong:
                if val > long_max_val:
                    long_max_val = val
            elif v.IsShort:
                if val > short_max_val:
                    short_max_val = val
            
    total_holdings = algorithm.Portfolio.TotalHoldingsValue
    long_pos = long_max_val / total_holdings
    short_pos = short_max_val / total_holdings
    algorithm.Plot('Position Concentration', 'Largest Long Position', long_pos)
    algorithm.Plot('Position Concentration', 'Largest Short Position', short_pos)
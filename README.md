# Offsetting U.S. Tariffs on Canadian Softwood Lumber: A DSGE Analysis of Domestic Subsidies

**Author:** Andrew Norris

## Abstract

The United States has imposed increasing tariffs on softwood lumber exports from Canada. In order to offset the effect of the tariffs, this paper proposes a direct subsidy for domestic softwood lumber usage in the construction industry. Using a small open dynamic stochastic general equilibrium model, we can model the subsidy's ability to offset the loss of export demand. By exploring the relationship of softwood lumber to Canada's economy and demand from the United States, we can calibrate the model to simulate the softwood lumber industry. The model will stimulate output from softwood lumber from sawmills, towards construction firms. The efficacy of this policy can be determined by comparing the effect of a negative shock on demand with or without the policy. This policy will have the secondary effect of increasing the housing stock in Canada, at a time where the country is facing a housing crisis.

## Project Structure

### `data-python/`
Contains Python scripts for data analysis and visualization, along with raw data files from Statistics Canada and other sources.

- **Data Processing Scripts:**
  - `generate_all_graphs.py` - Master script to generate all visualizations
  - Various specialized analysis scripts for different economic indicators

- **Economic Data Analysis:**
  - `canada-housing-starts/` - Canadian housing starts data and analysis
  - `employment/` - Sawmill employment data and trends
  - `exports/` - Lumber export data and U.S.-Canada trade analysis
  - `gdp/` - GDP data for forestry and related industries
  - `lumber-output/` - Lumber production and productivity analysis
  - `prices/` - Lumber and construction material price data
  - `sawmill-revenue/` - Sawmill industry revenue analysis
  - `tariffs/` - U.S. tariff data and timeline analysis

- **Chat Log Files:**
  - `chat.json`, `latex-formatting.json`, `table-latex.json` - Logs on VSCode AI Usage

### `images/`
Generated figures and charts from the data analysis scripts.

### `latex-paper/`
LaTeX document source files for the academic paper.

- `main.tex` - Main paper document
- `appendix.tex` - Supplementary material and model details
- `theoretical_model.tex` - DSGE model specification
- `references.bib` - Bibliography
- `figures/` - Figure files for inclusion in the paper

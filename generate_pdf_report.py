
import sys, pytest, collections, collections.abc, urllib3.exceptions, _pytest.pytester, numpy;
collections.Mapping = collections.abc.Mapping;
collections.MutableMapping = collections.abc.MutableMapping;
collections.MutableSet = collections.abc.MutableSet;
collections.Sequence = collections.abc.Sequence;
collections.Callable = collections.abc.Callable;
collections.Iterable = collections.abc.Iterable;
collections.Iterator = collections.abc.Iterator;
urllib3.exceptions.SNIMissingWarning = urllib3.exceptions.DependencyWarning;
pytest.RemovedInPytest4Warning = DeprecationWarning;
_pytest.pytester.Testdir = _pytest.pytester.Pytester;
numpy.PINF = numpy.inf;
numpy.unicode_ = numpy.str_;
numpy.bytes_ = numpy.bytes_;
numpy.float_ = numpy.float64;
numpy.string_ = numpy.bytes_;
numpy.NaN = numpy.nan;


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import warnings
warnings.filterwarnings('ignore')

# Load data and models
df = pd.read_csv('bittensor_subnet_data.csv')

# Prepare data for models
independent_vars = [
    'validator_count', 'miner_count', 'api_calls_per_day', 'total_stake',
    'network_activity', 'immunity_status', 'pruning_rank', 'ecosystem_routing',
    'revenue_per_validator', 'uptime_percentage', 'block_production_rate',
    'unique_miners', 'delegation_count', 'avg_validator_stake'
]

X = df[independent_vars]
X_const = sm.add_constant(X)
y_price = df['subnet_price']
y_emissions = df['emissions_tao']

# Fit models
model_price = sm.OLS(y_price, X_const).fit()
model_emissions = sm.OLS(y_emissions, X_const).fit()

# Create PDF report
doc = SimpleDocTemplate("bittensor_regression_analysis.pdf", pagesize=A4)
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    spaceAfter=30,
    alignment=TA_CENTER
)

section_style = ParagraphStyle(
    'Section',
    parent=styles['Heading2'],
    fontSize=16,
    spaceAfter=12,
    alignment=TA_LEFT
)

subsection_style = ParagraphStyle(
    'Subsection',
    parent=styles['Heading3'],
    fontSize=14,
    spaceAfter=8,
    alignment=TA_LEFT
)

normal_style = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=6,
    alignment=TA_JUSTIFY
)

# Build document content
story = []

# Title
story.append(Paragraph("Bittensor Subnet Regression Analysis", title_style))
story.append(Paragraph("Price and Emission Drivers Study", styles['Title']))
story.append(Spacer(1, 0.5*inch))

# Executive Summary
story.append(Paragraph("Executive Summary", section_style))
summary_text = f"""
<p>This report presents a comprehensive regression analysis of Bittensor subnet pricing and emission mechanisms. 
Two distinct multiple linear regression models were developed to identify the key drivers influencing subnet prices 
and emissions respectively.</p>

<p><b>Key Findings:</b></p>
<ul>
<li>The emission model demonstrates exceptional explanatory power with an R-squared of {model_emissions.rsquared:.3f}</li>
<li>The price model explains {model_price.rsquared:.1%} of the variance in subnet prices</li>
<li>Revenue per validator emerges as the strongest driver for emissions (coefficient: {model_emissions.params['revenue_per_validator']:.3f})</li>
<li>Block production rate is the second most influential factor for emissions (coefficient: {model_emissions.params['block_production_rate']:.3f})</li>
<li>Pruning rank negatively impacts emissions, suggesting poorly performing subnets receive fewer rewards</li>
</ul>
""" 
story.append(Paragraph(summary_text, normal_style))
story.append(Spacer(1, 0.3*inch))

# Methodology
story.append(Paragraph("Methodology", section_style))
num_subnets = len(df)
num_vars = len(independent_vars)
methodology_text = f"""
<p>This analysis employed multiple linear regression to examine relationships between subnet characteristics 
and both price formation and emission distribution. The dataset comprises {num_subnets} synthetic subnets 
with {num_vars} independent variables representing various aspects of subnet performance 
and network metrics.</p>

<p><b>Independent Variables Analyzed:</b></p>
<ul>
<li>Validator Count - Number of active validators</li>
<li>Miner Count - Number of participating miners</li>
<li>API Calls per Day - Network usage metrics</li>
<li>Total Stake - Aggregate TAO staked in the subnet</li>
<li>Network Activity Score - Composite measure of subnet engagement</li>
<li>Immunity Status - Binary indicator of subnet protection status</li>
<li>Pruning Rank - Performance ranking affecting subnet viability</li>
<li>Ecosystem Routing - Cross-subnet utilization metrics</li>
<li>Revenue per Validator - Economic incentives</li>
<li>Uptime Percentage - Reliability measure</li>
<li>Block Production Rate - Consensus participation</li>
<li>Unique Miners - Diversity of participant base</li>
<li>Delegation Count - Community trust indicators</li>
<li>Average Validator Stake - Capital commitment levels</li>
</ul>
"""
story.append(Paragraph(methodology_text, normal_style))
story.append(Spacer(1, 0.3*inch))

# Model 1: Price Analysis
story.append(Paragraph("Model 1: Subnet Price Drivers", section_style))
price_text = f"""
<p>The subnet price regression model yielded an R-squared of {model_price.rsquared:.3f}, indicating that approximately 
{model_price.rsquared:.1%} of the variance in subnet prices can be explained by the selected independent variables. 
The adjusted R-squared of {model_price.rsquared_adj:.3f} accounts for the model complexity.</p>

<p>The F-statistic of {model_price.fvalue:.2f} with a p-value of {model_price.f_pvalue:.2e} suggests the overall model 
is statistically significant at conventional levels.</p>
"""
story.append(Paragraph(price_text, normal_style))

# Significant Price Drivers
story.append(Paragraph("Significant Price Drivers (p < 0.05)", subsection_style))

# Get significant coefficients for price model
price_coef = model_price.params[1:]  # Exclude intercept
price_pvalues = model_price.pvalues[1:]
price_sig_coef = price_coef[price_pvalues < 0.05]

if len(price_sig_coef) > 0:
    story.append(Paragraph(f"<p>{len(price_sig_coef)} variables showed statistical significance (p < 0.05) in driving subnet prices:</p>", normal_style))
    
    # Create table of significant coefficients
    price_data = [['Variable', 'Coefficient', 'P-value']]
    for var, coef in price_sig_coef.sort_values(key=abs, ascending=False).items():
        pval = price_pvalues[var]
        price_data.append([var, f"{coef:.4f}", f"{pval:.4f}"])
    
    price_table = Table(price_data)
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(price_table)
else:
    story.append(Paragraph("<p>No variables achieved statistical significance (p < 0.05) in explaining subnet price variation.</p>", normal_style))

story.append(Spacer(1, 0.2*inch))

# Model 2: Emissions Analysis
story.append(PageBreak())
story.append(Paragraph("Model 2: Emission Drivers", section_style))
emissions_text = f"""
<p>The emission regression model demonstrates exceptional explanatory power with an R-squared of {model_emissions.rsquared:.3f}. 
This indicates that {model_emissions.rsquared:.1%} of the variance in subnet emissions can be attributed to the 
independent variables included in the model. The adjusted R-squared of {model_emissions.rsquared_adj:.3f} confirms 
the model's robustness despite its complexity.</p>

<p>The F-statistic of {model_emissions.fvalue:.2f} with a highly significant p-value of {model_emissions.f_pvalue:.2e} 
confirms that the model as a whole provides substantial explanatory power for emission dynamics.</p>
"""
story.append(Paragraph(emissions_text, normal_style))

# Significant Emission Drivers
story.append(Paragraph("Significant Emission Drivers (p < 0.05)", subsection_style))

# Get significant coefficients for emissions model
emissions_coef = model_emissions.params[1:]  # Exclude intercept
emissions_pvalues = model_emissions.pvalues[1:]
emissions_sig_coef = emissions_coef[emissions_pvalues < 0.05]

story.append(Paragraph(f"<p>{len(emissions_sig_coef)} variables showed statistical significance (p < 0.05) in driving subnet emissions:</p>", normal_style))

# Create table of significant coefficients
emissions_data = [['Variable', 'Coefficient', 'P-value']]
for var, coef in emissions_sig_coef.sort_values(key=abs, ascending=False).items():
    pval = emissions_pvalues[var]
    emissions_data.append([var, f"{coef:.4f}", f"{pval:.4f}"])

emissions_table = Table(emissions_data)
emissions_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
story.append(emissions_table)

story.append(Spacer(1, 0.2*inch))

# Key Insights
story.append(Paragraph("Key Insights and Conclusions", section_style))
insights_text = f"""
<p><b>Most Important Emission Drivers:</b></p>
<ol>
<li><b>Revenue per Validator</b>: The strongest positive driver of emissions (β = {model_emissions.params['revenue_per_validator']:.3f}), suggesting that economically 
successful subnets receive proportionally higher rewards. This creates a positive feedback loop where successful 
subnets attract more investment and resources.</li>

<li><b>Block Production Rate</b>: Strong positive relationship (β = {model_emissions.params['block_production_rate']:.3f}) indicates that active participation in 
consensus mechanisms directly correlates with reward allocation.</li>

<li><b>Pruning Rank</b>: Negative coefficient (β = {model_emissions.params['pruning_rank']:.3f}) reveals that poorly performing subnets face reduced 
reward distributions, enforcing network quality standards.</li>

<li><b>Network Activity</b>: Positive impact (β = {model_emissions.params['network_activity']:.3f}) shows that engaged subnets with higher activity levels 
receive preferential treatment in emission distributions.</li>
</ol>

<p><b>Price Formation Dynamics:</b></p>
<p>While the price model shows lower explanatory power, the marginal significance of immunity status (p = {model_price.pvalues['immunity_status']:.3f}) 
suggests that market participants value subnet protection and stability. This aligns with economic theory where 
protected assets command premium valuations due to reduced risk exposure.</p>

<p><b>Network Design Implications:</b></p>
<p>The stark contrast between emission and price model performance suggests that emission mechanisms are 
primarily algorithmic and transparent, while price formation incorporates numerous external market factors 
beyond the scope of on-chain metrics.</p>
"""
story.append(Paragraph(insights_text, normal_style))

# Appendices with Charts
story.append(PageBreak())
story.append(Paragraph("Appendix A: Model Performance Visualizations", section_style))

# Add charts
story.append(Paragraph("Figure 1: Actual vs Predicted Values", subsection_style))
story.append(Image('actual_vs_predicted.png', width=6*inch, height=2.5*inch))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Figure 2: Residual Analysis", subsection_style))
story.append(Image('residual_plots.png', width=6*inch, height=2.5*inch))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Figure 3: Significant Coefficient Analysis", subsection_style))
story.append(Image('significant_coefficients.png', width=6*inch, height=3*inch))
story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Figure 4: Variable Distributions", subsection_style))
story.append(Image('distributions.png', width=6*inch, height=2.5*inch))

# Build PDF
doc.build(story)
print("PDF report generated successfully: bittensor_regression_analysis.pdf")
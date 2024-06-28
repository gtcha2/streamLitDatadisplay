import pandas as pd
# the goal should be to output 1, a data frame that strips the following, incorrect values and empty ones....
# I will be evaluating the difference between human responders and models... vision vs non vision. ... 
# should I run a base line case example? no baseline stuff exists. 

class ExcelFormatter:

    def __init__(self,excel_path):
        self.excel_df=pd.read_excel(excel_path)
        
    def __str__(self):
        return f'DataFrame{self.excel_df}'





path="/Users/aaronfanous/Documents/MisinformationFiles/MisinformationRepo/streamLitDatadisplay/data/raw/HumanRepsonsesRaw/PromptSysReviewPresentation.xlsx"      
formatter=ExcelFormatter(path)
print(formatter.excel_df['Does this post have visible image or working url to image?'].unique())

# the next steps i have to do are the following 
# the following